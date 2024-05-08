from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from simulation import Simulation
from server import Server
from user import User


class SysState(object):

    """
    SysState contains the state of the system, including the simulation object, current timestamp and stop flag,
    indicating whether the simulation is still running. In addition, it contains the objects for servers and users that
    correspond to simulation parameters, current number of packets in a buffer and number of dropped and total packets.
    """

    def __init__(self, sim: Simulation):
        """
        Generate SysState objects and initialize variables.
        :param sim: simulation object
        """
        self.sim = sim
        self.now = 0
        self.stop = False
        self.packets_dropped = 0
        self.packets_total = 0
        self.server = Server(sim, sim.sim_param.SERVICE_RATE)
        self.user = User(sim, sim.sim_param.ARRIVAL_RATE)
        self.buffer_content = 0

    def reset(self):
        """
        Reset SysState object, including the generation of servers and users objects.
        """
        self.now = 0
        self.stop = False
        self.packets_dropped = 0
        self.packets_total = 0
        self.buffer_content = 0
        self.server.reset(self.sim.sim_param.SERVICE_RATE)
        self.user.reset(self.sim.sim_param.ARRIVAL_RATE)

    def packet_entered(self):
        """
        Count a packet that has entered the system (queue or server).
        """
        self.packets_total += 1

    def packet_dropped(self):
        """
        Count a packet that has been rejected due to full buffer.
        """
        self.packets_dropped += 1

    def get_blocking_probability(self):
        """
        Get the blocking probability throughout the simulation.
        :return: blocking probability of the system
        """
        return self.packets_dropped/self.packets_total

    def start_users(self):
        """
        Start generating packets by users
        """
        self.user.generate_packet_arrival()
        # 1.1.6 ????

    def add_packet_to_buffer(self):
        """
        Attempt to add packet to buffer.
        :return: - True if could add packet to buffer, false if buffer is full
        """
        #######################################
        # TODO Task 1.1.1: Your code goes here
        try:
            self.buffer_content += 1
            return True
        except:
            return False
        
        pass
        #######################################

    def start_serving_packet(self):
        """
        Attempt to start service of newly arrived packet.
        :return: - False if server is busy, true if successfully started service
        """
        #######################################
        # TODO Task 1.1.5: Your code goes here
        if self.buffer_content == 0:
            return self.server.start_service(self, pkt_arrived=True)
        else:
            return False
        pass
        #######################################



