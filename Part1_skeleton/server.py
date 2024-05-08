from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from simulation import Simulation


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
        # TODO Task 1.1.2: Your code goes here

        self.service_rate = service_rate
        self.sim = sim
        self.server_busy = False
        pass
        #######################################

    def reset(self, service_rate: float):
        """
        reset Server object
        """
        #######################################
        # TODO Task 1.1.2: Your code goes here
        self.server_busy = True
        self.service_rate = service_rate
        pass
        #######################################

    def start_service(self, pkt_arrived: bool = False):
        """
        Start service by the server.
        :param pkt_arrived: if true, a new packet arrived to the empty system and should be served directly;
        if false, the packet from buffer should be served if the buffer is not empty
        :return: True if server starts the service, false if server was busy or there is no packet to serve
        """
        #######################################
        # TODO Task 1.1.3: Your code goes here
        if self.server_busy:
            self.buffer_content += 1
            return False
        elif ~pkt_arrived:
            return False
        else:
            self.server_busy = True
            return True

        pass
        #######################################


    def complete_service(self):
        """
        Reset server status to idle after a service completion.
        """
        #######################################
        # TODO Task 1.1.4: Your code goes here
        self.server_busy = False
        pass
        #######################################

    def generate_service_completion(self):
        """
        Generate next service completion event and insert it to event chain
        """
        #######################################
        # TODO Task 1.3.3: Your code goes here
        pass
        #######################################



