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
        self.initialized = False

    def reset(self):
        """
        Reset the Simulation object.
        """
        self.sys_state.reset()
        self.event_chain = EventChain()
        self.statistics_collection.reset()
        self.initialized = False

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


    # TODO Task 5.2.2: Modify the function below according to the task description
    # (change declaration if required, e.g., add a flag indicating that the simulation starts from scratch)
    def do_simulation_n_limit(self, n: int):
        """
        Call this function, if the simulation should stop after a given number of packets
        Do one simulation run. Initialize simulation and create first event.
        After that, one after another event is processed.
        :param n: number of customers, that are processed before the simulation stops
        :param new_run: flag indicating that the simulation starts from the very beginning
        :return: SimResult object
        """
        #######################################
        # DONE Task 4.3.3:
        if not self.initialized:
            self.sys_state.start_users()
            self.initialized = True
        cnt_served_packets = 0

        # start simulation (run)
        while cnt_served_packets < n:
            if not self.event_chain.event_list:
                self.sys_state.stop = True
                break

            e = self.event_chain.remove_oldest_event()
            if e:
                # if event exists and timestamps are ok, process the event
                if self.sys_state.now <= e.timestamp:
                    self.sys_state.now = e.timestamp
                    self.statistics_collection.count_queue_and_servers(self.sys_state.now)
                    e.process()

                    # if this event is a service completion event
                    if e.order == 0:
                        cnt_served_packets += 1
                        if cnt_served_packets > n:
                            self.sys_state.stop = True
                else:
                    print("NOW: " + str(self.sys_state.now) + ", EVENT TIMESTAMP: " + str(e.timestamp))
                    raise RuntimeError("ERROR: TIMESTAMP OF EVENT IS SMALLER THAN CURRENT TIME.")

            else:
                print("Event chain is empty. Abort")
                self.sys_state.stop = True
        self.statistics_collection.gather_results()
        return self.statistics_collection
        #######################################


