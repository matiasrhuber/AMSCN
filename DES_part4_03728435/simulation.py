from systemstate import SysState
from event import EventChain, SimulationTermination
from simparam import SimParam
from statisticscollection import StatCollection


class Simulation(object):

    def __init__(self, sim_param=SimParam()):
        """
        Initialize the Simulation object.
        :param sim_param: is an optional SimParam object for parameter pre-configuration; if not specified, default
        parameters from the SimParam constructor are used
        """
        self.sim_param = sim_param
        self.sys_state = SysState(self)
        self.event_chain = EventChain()
        self.statistics_collection = StatCollection(self)

    def reset(self):
        """
        Reset the Simulation object.
        """
        self.sys_state.reset()
        self.event_chain = EventChain()
        self.statistics_collection.reset()

    def do_simulation(self):
        """
        Do one simulation run. Initialize simulation and users, create last event.
        After that, one after another event is processed.
        :return: StatCollection object
        """
        # users starts generating packets and last event is inserted
        self.sys_state.start_users()
        self.event_chain.insert(SimulationTermination(self, self.sim_param.SIM_TIME))

        # start simulation (run)
        while not self.sys_state.stop:
            # get next simevent from events
            e = self.event_chain.remove_oldest_event()
            if e:
                # if event exists and timestamps are ok, process the event
                if self.sys_state.now <= e.timestamp:
                    self.sys_state.now = e.timestamp
                    self.statistics_collection.count_queue_and_servers(self.sys_state.now)
                    e.process()
                else:
                    print("NOW: " + str(self.sys_state.now) + ", EVENT TIMESTAMP: " + str(e.timestamp))
                    raise RuntimeError("ERROR: TIMESTAMP OF EVENT IS SMALLER THAN CURRENT TIME.")

            else:
                print("Event chain is empty. Abort")
                self.sys_state.stop = True
        self.statistics_collection.gather_results()
        return self.statistics_collection

    def do_simulation_n_limit(self, n):
        """
        Call this function, if the simulation should stop after a given number of packets
        Do one simulation run. Initialize simulation and create first event.
        After that, one after another event is processed.
        :param n: number of customers, that are processed before the simulation stops
        :return: SimResult object
        """
        # insert first event only if no new batch has been started
        #######################################
        # TODO Task 4.3.3: Your code goes here


            # users starts generating packets and last event is inserted
        self.sys_state.start_users()
        self.event_chain.insert(SimulationTermination(self, self.sim_param.SIM_TIME))

        # start simulation (run)
        while not self.sys_state.stop and self.statistics_collection.packets_served < n:
            # get next simevent from events
            e = self.event_chain.remove_oldest_event()
            if e:
                # if event exists and timestamps are ok, process the event
                if self.sys_state.now <= e.timestamp:
                    self.sys_state.now = e.timestamp
                    self.statistics_collection.count_queue_and_servers(self.sys_state.now)
                    e.process()
                else:
                    print("NOW: " + str(self.sys_state.now) + ", EVENT TIMESTAMP: " + str(e.timestamp))
                    raise RuntimeError("ERROR: TIMESTAMP OF EVENT IS SMALLER THAN CURRENT TIME.")

            else:
                print("Event chain is empty. Abort")
                self.sys_state.stop = True
        self.statistics_collection.gather_results()
        return self.statistics_collection
        #######################################


