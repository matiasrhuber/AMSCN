from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from simulation import Simulation
from event import PacketArrival
import random
from packet import Packet
from rns import ExponentialRNS, UniformRNS
from simparam import ARR_PROCESS

class User(object):
    """
    This class represents the user.
    It contains information about the simulation object it belongs to
    and avg arrival rate of the user in pkt/ms. (rate[pkt/ms] = 1 / mean[ms])
    """

    # TODO Task 3.1.3: Correct function declaration according to task description.
    def __init__(self, sim: Simulation, arrival_rate: float,  seed: float=None):
        """
        Create a user object
        :param arrival_rate: parameter for the arrival rate - how many packets arrive in millisecond
        """
        self.sim = sim
        self.arrival_rate = arrival_rate
        self.last_iat = None
        #######################################
        # TODO Task 3.1.3: Your code goes here.
        if self.sim.sim_param.USERS_ARRIVAL_PROCESS == ARR_PROCESS.EXPONENTIAL:
            self.ia_time_generator = ExponentialRNS(1 / arrival_rate, seed)
        elif self.sim.sim_param.USERS_ARRIVAL_PROCESS == ARR_PROCESS.UNIFORM:
            # Set the parameters for the Uniform distribution
            a = 1 / arrival_rate - (1 / arrival_rate) * 0.1
            b = 1 / arrival_rate + (1 / arrival_rate) * 0.1
            self.ia_time_generator = UniformRNS(a, b, seed)
        #######################################

    # TODO Task 3.1.3: Correct function declaration according to task description.
    def reset(self, arrival_rate: float, seed: float=None):
        """
        reset User object
        """
        #######################################
        # TODO Task 3.1.3: Your code goes here.
        if self.arrival_rate != arrival_rate:
            if ARR_PROCESS == 'Exponential':
                self.ia_time_generator = ExponentialRNS(1 / arrival_rate, seed)
            elif ARR_PROCESS == 'Uniform':
                a = 1 / arrival_rate - (1 / arrival_rate) * 0.1
                b = 1 / arrival_rate + (1 / arrival_rate) * 0.1
                self.ia_time_generator = UniformRNS(a, b, seed)
            else:
                raise ValueError("Unsupported arrival process specified in simparam.py")
        #######################################
        self.arrival_rate = arrival_rate
        self.last_iat = None

    def generate_packet_arrival(self):
        """
        Create next packet arrival event and insert it to the event chain
        """
        # generate and store (for statistics) inter-arrival time for the next packet
        #######################################
        # TODO Task 3.1.3: Modify code below
        # self.last_iat = random.uniform(1, 2 / self.arrival_rate)
        # # generate next packet arrival event and insert it to event chain
        # ev = PacketArrival(self.sim, self.sim.sys_state.now + self.last_iat, self)
        # self.sim.event_chain.insert(ev)
        self.last_iat = self.ia_time_generator.next()
        ev = PacketArrival(self.sim, self.sim.sys_state.now + self.last_iat, self)
        self.sim.event_chain.insert(ev)
        #######################################

    def generate_packet(self):
        """
        Generate new packet.
        :return packet generated with timestamp now
        """
        #######################################
        # DONE Task 2.2.3:
        # Generate packet with timestamp now
        pkt = Packet(self.sim.sys_state.now, self)
        return pkt
        #######################################
