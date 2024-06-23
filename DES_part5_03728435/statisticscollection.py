from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from simulation import Simulation
    from packet import Packet
from counter import TimeIndependentCounter, TimeDependentCounter, TimeIndependentAutocorrelationCounter,\
    TimeIndependentCrosscorrelationCounter


class StatCollection(object):
    """
    StatCollection is a collection of all counters that are used in the simulations.

    It contains several counters, that are used in the different tasks.
    Reporting function can be adapted depending on which counters should
    report their results.
    """

    def __init__(self, sim: Simulation):
        """
        Initialize the counter collection.
        :param sim: the simulation, the CounterCollection belongs to.
        """
        self.sim = sim

        self.sim = sim
        self.packets_dropped = 0
        self.packets_served = 0
        self.packets_total = 0
        self.mean_waiting_time = 0
        self.mean_queue_length = 0
        self.blocking_probability = 0
        self.mean_number_busy_servers = 0

        # waiting time
        self.cnt_wt = TimeIndependentCounter("wt")

        # queue length
        self.cnt_ql = TimeDependentCounter("ql")

        # number of busy servers
        self.cnt_bs = TimeDependentCounter("bs")

        self.cnt_iat = TimeIndependentCounter("iat")

        #######################################
        self.acnt_wt = TimeIndependentAutocorrelationCounter("waiting time with lags 1 to 20", max_lag=20)
        self.acnt_iat = TimeIndependentAutocorrelationCounter("accumulated iat with lags 1 to 10")

        self.cnt_iat_wt = TimeIndependentCrosscorrelationCounter("inter-arrival time vs. waiting time")
        self.cnt_iat_st = TimeIndependentCrosscorrelationCounter("inter-arrival time vs. service time")
        self.cnt_iat_syst = TimeIndependentCrosscorrelationCounter("inter-arrival time vs. system time")
        self.cnt_st_syst = TimeIndependentCrosscorrelationCounter("service time vs. system time")

        self.cnt_wt1_wt2 = TimeIndependentCrosscorrelationCounter("wt user 1 vs. wt user 2")
        self.cnt_wt1 = TimeIndependentCounter("wt user 1")
        self.cnt_wt2 = TimeIndependentCounter("wt user 2")
        #######################################

    def reset(self):
        """
        Resets all counters.
        """
        self.cnt_wt.reset()
        self.cnt_ql.reset()
        self.cnt_bs.reset()
        self.cnt_iat.reset()

        #######################################
        self.acnt_wt.reset()
        self.acnt_iat.reset()

        self.cnt_iat_wt.reset()
        self.cnt_iat_st.reset()
        self.cnt_iat_syst.reset()
        self.cnt_st_syst.reset()
        self.cnt_wt1_wt2.reset()
        self.cnt_wt1.reset()
        self.cnt_wt2.reset()
        #######################################

    def report(self):
        """
        Calls the report function of the counters.
        Can be adapted, such that not all reports are printed
        """
        self.cnt_wt.report()
        self.cnt_ql.report()
        self.cnt_bs.report()
        #######################################
        self.acnt_wt.report()
        self.acnt_iat.report()
        self.cnt_iat_wt.report()
        self.cnt_iat_st.report()
        self.cnt_iat_syst.report()
        self.cnt_st_syst.report()
        self.cnt_wt1_wt2.report()
        #######################################

    def count_packet(self, packet: Packet):
        """
        Count a packet. Its data is counted by the various counters.
        """
        self.cnt_wt.count(packet.get_waiting_time())
        #######################################
        self.acnt_wt.count(packet.get_waiting_time())

        self.cnt_iat_wt.count(packet.get_inter_arrival_time(), packet.get_waiting_time())
        self.cnt_iat_st.count(packet.get_inter_arrival_time(), packet.get_service_time())
        self.cnt_iat_syst.count(packet.get_inter_arrival_time(), packet.get_system_time())
        self.cnt_st_syst.count(packet.get_service_time(), packet.get_system_time())

        if self.sim.sim_param.NUM_USERS >= 2:
            if packet.user == self.sim.sys_state.users[0]:
                self.cnt_wt1.count(packet.get_waiting_time())
            if packet.user == self.sim.sys_state.users[1]:
                self.cnt_wt2.count(packet.get_waiting_time())
        #######################################

    def count_queue_and_servers(self, now: float):
        """
        Count the number of packets in the buffer and add the values to the corresponding (time dependent) counter.
        This function should be called at least whenever the number of packets in the buffer changes.

        The offered traffic is counted as well and can be counted from the counter cnt_ot.

        :param now: current simulation time
        """
        self.cnt_ql.count(self.sim.sys_state.buffer.get_queue_length(), now)

        busy_servers = 0
        for server in self.sim.sys_state.servers:
            if server.server_busy:
                busy_servers += 1
        self.cnt_bs.count(busy_servers, now)

    def count_iat(self, iat: float):
        """
        Count global inter-arrival time
        :param iat: iat to be counter
        """
        self.cnt_iat.count(iat)
        self.acnt_iat.count(iat)

    def gather_results(self):
        """
        Gather all available simulation results from SysState and StatisticsCollection
        """
        try:
            self.mean_number_busy_servers = self.sim.statistics_collection.cnt_bs.get_mean()
            self.mean_waiting_time = self.sim.statistics_collection.cnt_wt.get_mean()
            self.mean_queue_length = self.sim.statistics_collection.cnt_ql.get_mean()
        except:
            print("counter_collection not available for getting simulation results.")
            pass
        self.packets_dropped = self.sim.sys_state.packets_dropped
        self.packets_served = self.sim.sys_state.packets_total - self.sim.sys_state.packets_dropped
        self.packets_total = self.sim.sys_state.packets_total
        self.blocking_probability = self.sim.sys_state.get_blocking_probability()

        ######################################
        if self.sim.sim_param.NUM_USERS >= 2:
            for i in range(min(len(self.cnt_wt1.values), len(self.cnt_wt2.values))):
                self.cnt_wt1_wt2.count(self.cnt_wt1.values[i], self.cnt_wt2.values[i])
        ######################################