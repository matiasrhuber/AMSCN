from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from simulation import Simulation
from event import ServiceCompletion
from packet import Packet
from rns import ExponentialRNS


class Server(object):
    """
    This class represents the server.

    It contains information about service rate and whether the server is busy.
    """

    def __init__(self, sim: Simulation, service_rate: float, seed: float = None):
        """
        Create a server object
        :param service_rate: parameter for the service rate - how many packets are served in millisecond
        (rate[pkt/ms] = 1 / mean_service_time[ms])
        :param sim: Simulation object the server belongs to
        :param seed: optional seed for RNS
        """
        self.sim = sim
        self.server_busy = False
        self.service_rate = service_rate

        self.packet_in_service = None

        #######################################
        # DONE Task 3.1.2:
        self.service_time_generator = ExponentialRNS(service_rate, seed)
        #######################################

    def reset(self, service_rate: float, seed: float):
        """
        reset Server object
        :param service_rate: parameter for the service rate - how many packets are served in millisecond
        :param seed: optional seed for RNS
        """
        #######################################
        # DONE Task 3.1.2:
        if service_rate != self.service_rate:
            self.service_time_generator = ExponentialRNS(service_rate, seed)
        #######################################
        self.service_rate = service_rate

        self.packet_in_service = None
        self.server_busy = False

    def start_service(self, pkt_arrived: Packet = None):
        """
        Start service by the server.
        :param pkt_arrived: if not None, specifies the packet to be served
        :return: True if server starts the service, false if server was busy or there is no packet to serve
        """
        # Return false if server is currently busy.
        if self.server_busy:
            return False
        else:
            # If no packet to be served specified, try to pull packet from buffer
            if pkt_arrived is None:
                pkt_arrived = self.sim.sys_state.buffer.remove()
            # If could pull packet from buffer or packet to be served is specified, start service of this packet
            if pkt_arrived is not None:
                self.packet_in_service = pkt_arrived
                self.packet_in_service.start_service(self.sim.sys_state.now)
                self.server_busy = True
                self.generate_service_completion()
                return True
            return False

    def complete_service(self):
        """
        Reset server status to idle after a service completion.
        """
        if self.server_busy is False:
            raise RuntimeError("ERROR: TRYING TO COMPLETE SERVICE, BUT NO PACKET WAS IN SERVICE.")
        self.server_busy = False
        # take packet that was in service and complete its service
        p = self.packet_in_service
        p.complete_service(self.sim.sys_state.now)
        self.packet_in_service = None

        self.sim.statistics_collection.count_packet(p)

    def generate_service_completion(self):
        """
        Generate next service completion event and insert it to event chain
        """
        #######################################
        # DONE Task 3.1.2:
        st = self.service_time_generator.next()
        ev = ServiceCompletion(self.sim, self.sim.sys_state.now + st, self)
        self.sim.event_chain.insert(ev)
        #######################################



