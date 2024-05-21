from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from simulation import Simulation
from event import PacketArrival
import random
from packet import Packet


class User(object):
    """
    This class represents the user.
    It contains information about the simulation object it belongs to
    and avg arrival rate of the user in pkt/ms. (rate[pkt/ms] = 1 / mean[ms])
    """

    def __init__(self, sim: Simulation, arrival_rate: float):
        """
        Create a user object
        :param arrival_rate: parameter for the arrival rate - how many packets arrive in millisecond
        """
        self.sim = sim
        self.arrival_rate = arrival_rate
        self.last_iat = None

    def reset(self, arrival_rate: float):
        """
        reset User object
        """
        self.arrival_rate = arrival_rate
        self.last_iat = None

    def generate_packet_arrival(self):
        """
        Create next packet arrival event and insert it to the event chain
        """
        #######################################
        # DONE Task 1.3.1: Your code goes here
        # generate and store (for statistics) inter-arrival time for the next packet
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
        # TODO Task 2.2.3: Your code goes here
        return Packet(arrival_time=self.sim.sys_state.now)
        #######################################
