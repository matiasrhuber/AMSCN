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
    def __init__(self, sim: Simulation, arrival_rate: float):
        """
        Create a user object
        :param arrival_rate: parameter for the arrival rate - how many packets arrive in millisecond
        """
        self.sim = sim
        self.arrival_rate = arrival_rate
        self.last_iat = None
        #######################################
        # TODO Task 3.1.3: Your code goes here.
        pass
        #######################################

    # TODO Task 3.1.3: Correct function declaration according to task description.
    def reset(self, arrival_rate: float):
        """
        reset User object
        """
        #######################################
        # TODO Task 3.1.3: Your code goes here.
        pass
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
        self.last_iat = random.uniform(1, 2 / self.arrival_rate)
        # generate next packet arrival event and insert it to event chain
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
