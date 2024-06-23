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

    def __init__(self, sim: Simulation, arrival_rate: float, seed: float = None):
        """
        Create a user object
        :param arrival_rate: parameter for the arrival rate - how many packets arrive in millisecond
        """
        self.sim = sim
        self.arrival_rate = arrival_rate
        self.last_iat = None
        #######################################
        # DONE Task 3.1.3:
        if sim.sim_param.USERS_ARRIVAL_PROCESS == ARR_PROCESS.UNIFORM:
            self.ia_time_generator = UniformRNS(1, 2 / arrival_rate, seed)
        elif sim.sim_param.USERS_ARRIVAL_PROCESS == ARR_PROCESS.EXPONENTIAL:
            self.ia_time_generator = ExponentialRNS(arrival_rate, seed)
        #######################################

    def reset(self, arrival_rate: float, seed: float):
        """
        reset User object
        """
        #######################################
        # DONE Task 3.1.3:
        if arrival_rate != self.arrival_rate:
            if self.sim.sim_param.USERS_ARRIVAL_PROCESS == ARR_PROCESS.UNIFORM:
                self.ia_time_generator = UniformRNS(1, 2 / arrival_rate, seed)
            elif self.sim.sim_param.USERS_ARRIVAL_PROCESS == ARR_PROCESS.EXPONENTIAL:
                self.ia_time_generator = ExponentialRNS(arrival_rate, seed)
        #######################################
        self.arrival_rate = arrival_rate
        self.last_iat = None

    def generate_packet_arrival(self):
        """
        Create next packet arrival event and insert it to the event chain
        """
        # generate and store (for statistics) inter-arrival time for the next packet
        #######################################
        # DONE Task 3.1.3:
        self.last_iat = self.ia_time_generator.next()
        # generate next packet arrival event and insert it to event chain
        ev = PacketArrival(self.sim, self.sim.sys_state.now + self.last_iat, self)
        self.sim.event_chain.insert(ev)
        #######################################

    def generate_packet(self):
        """
        Generate new packet.
        :return packet generated with timestamp now
        """
        # Generate packet with timestamp now
        pkt = Packet(self.sim.sys_state.now, self)
        return pkt
