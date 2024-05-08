from systemstate import SysState
from event import EventChain, SimulationTermination
from simparam import SimParam


class Simulation(object):

    def __init__(self, sim_param: SimParam = SimParam()):
        """
        Initialize the Simulation object.
        :param sim_param: is an optional SimParam object for parameter pre-configuration; if not specified, default
        parameters from the SimParam constructor are used
        """
        self.sim_param = sim_param
        self.sys_state = SysState(self)
        self.event_chain = EventChain()

    def reset(self):
        """
        Reset the Simulation object.
        """
        self.sys_state.reset()
        self.event_chain = EventChain()

    def do_simulation(self):
        """
        Do one simulation run. Initialize simulation and users, create last event.
        After that, one after another event is processed.
        """
        # user starts generating packet and last event is inserted
        self.sys_state.start_users()
        self.event_chain.insert(SimulationTermination(self, self.sim_param.SIM_TIME))

        # start simulation (run)
        while not self.sys_state.stop:
            #######################################
            # TODO Task 1.4.1: Your code goes here
            pass
            #######################################



