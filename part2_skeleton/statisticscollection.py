from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from simulation import Simulation
    from packet import Packet
from counter import TimeIndependentCounter, TimeDependentCounter


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
        self.cnt_bs = TimeDependentCounter("ot")

    def reset(self):
        """
        Resets all counters and histograms.
        """
        self.cnt_wt.reset()
        self.cnt_ql.reset()
        self.cnt_bs.reset()

    def report(self):
        """
        Calls the report function of the counters and histograms.
        Can be adapted, such that not all reports are printed
        """
        self.cnt_wt.report()
        self.cnt_ql.report()
        self.cnt_bs.report()

    def count_packet(self, packet: Packet):
        """
        Count a packet. Its data is counted by the various counters.
        """
        #######################################
        # TODO Task 2.4.3: Your code goes here
        self.packets_total += 1
        if packet.t_start_service is not None:
            waiting_time = packet.t_start_service - packet.t_arrival
            self.cnt_wt.count(waiting_time)
        #######################################

    def count_queue_and_servers(self, now: float):
        """
        Count the number of packets in the buffer and add the values to the corresponding (time dependent) counter.
        This function should be called at least whenever the number of packets in the buffer changes.

        The offered traffic is counted as well and can be counted from the counter cnt_ot.

        :param now: current simulation time
        """
        ######################################
        # TODO Task 2.4.3: Your code goes here
        queue_length = len(self.sim.sys_state.buffer)
        self.cnt_ql.count(queue_length, now)
        busy_servers = sum(server.busy for server in self.sim.sys_state.servers)
        self.cnt_bs.count(busy_servers, now)
        #######################################

    def gather_results(self):
        """
        Gather all available simulation results from SimState and CounterCollection
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
