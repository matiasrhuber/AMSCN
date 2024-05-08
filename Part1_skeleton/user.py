from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from simulation import Simulation
import random
from event import PacketArrival

class User(object):
    """
    This class represents the user.
    It contains information about the simulation object it belongs to, last inter-arrival time of this packet
    (for statistics) avg arrival rate of the user in pkt/ms. (rate[pkt/ms] = 1 / mean[ms])
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
        # TODO Task 1.3.1: Your code goes here
        mean_iat = 1 / self.arrival_rate
        self.last_iat = random.uniform(1, 2*mean_iat)

        timestamp = self.sim.sys_state.time + self.last_iat
        packet_arrival_event = PacketArrival(self.sim, timestamp)
        self.sim.event_chain.insert(packet_arrival_event)

        pass
        #######################################
