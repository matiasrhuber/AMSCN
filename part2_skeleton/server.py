from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from simulation import Simulation
from event import ServiceCompletion
from packet import Packet


class Server(object):
    """
    This class represents the server.

    It contains information about service rate and whether the server is busy.
    """

    def __init__(self, sim: Simulation, service_rate: float):
        """
        Create a server object
        :param service_rate: parameter for the service rate - how many packets are served in millisecond
        (rate[pkt/ms] = 1 / mean_service_time[ms])
        :param sim: Simulation object the server belongs to
        """
        #######################################
        # DONE Task 1.1.2:
        self.sim = sim
        self.server_busy = False
        self.service_rate = service_rate
        #######################################

        #######################################
        # TODO Task 2.2.4: Your code goes here
        self.packet_in_service = None
        #######################################

    def reset(self, service_rate: float):
        """
        reset Server object
        :param service_rate: parameter for the service rate - how many packets are served in millisecond
        """
        #######################################
        # DONE Task 1.1.2:
        self.service_rate = service_rate
        self.server_busy = False
        #######################################

        #######################################
        # TODO Task 2.2.4: Your code goes here
        self.packet_in_service = None
        pass
        #######################################

    # TODO Task 2.2.4: Correct function declaration according to task description
    def start_service(self, pkt_arrived: Packet = None):
        """
        Start service by the server.
        :param pkt_arrived: if not None, specifies the packet to be served
        :return: True if server starts the service, false if server was busy or there is no packet to serve
        """
        # TODO Task 2.2.4: Comment code below
        #######################################
        # DONE Task 1.1.3:
        # Return false if server is currently busy.
        # if self.server_busy:
        #     return False
        # else:
        #     # If no packet arrived and should be served directly, check if there is a packet in buffer
        #     if not pkt_arrived:
        #         # If buffer is not empty, take packet from there
        #         if self.sim.sys_state.buffer_content:
        #             self.sim.sys_state.buffer_content -= 1
        #         # Return false if buffer is empty
        #         else:
        #             return False
        #     # If packet can be taken from buffer or new packet arrived, start service
        #     self.server_busy = True
        # # DONE Task 1.3.4:
        #     self.generate_service_completion()
        #     return True
        #######################################

        #######################################
        # TODO Task 2.2.4: Rewrite code from above, your code goes here
        if self.server_busy:
            return False
        else:
            if pkt_arrived is None:
                if self.sim.sys_state.buffer.is_empty():
                    return False
                else:
                    pkt_arrived = self.sim.sys_state.buffer.queue.get() # dequeue?

            
            self.server_busy = True
            self.packet_in_service = pkt_arrived
            pkt_arrived.start_service(self.sim.sys_state.now)
            self.generate_service_completion()
            return True
        pass
        #######################################

    def complete_service(self):
        """
        Reset server status to idle after a service completion.
        """
        #######################################
        # DONE Task 1.1.4:
        if self.server_busy is False:
            raise RuntimeError("ERROR: TRYING TO COMPLETE SERVICE, BUT NO PACKET WAS IN SERVICE.")
        self.server_busy = False
        #######################################
        # TODO Task 2.2.4: Your code goes here
        pass
        #######################################

        #######################################
        # TODO Task 2.4.3: Your code goes here
        pass
        #######################################

    def generate_service_completion(self):
        """
        Generate next service completion event and insert it to event chain
        """
        #######################################
        # DONE Task 1.3.3: Your code goes here
        ev = ServiceCompletion(self.sim, self.sim.sys_state.now + 1 / self.service_rate, self)
        self.sim.event_chain.insert(ev)
        #######################################



