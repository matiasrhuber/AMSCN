from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from simulation import Simulation
from server import Server
from user import User
from finitequeue import FiniteQueue
from packet import Packet


class SysState(object):

    """
    SysState contains the state of the system, including the simulation object, current timestamp and stop flag,
    indicating whether the simulation is still running. In addition, it contains the objects for servers and users that
    correspond to simulation parameters, a buffer and number of dropped and total packets.
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
        # TODO Task 2.3.1: comment these lines
        #######################################
        # self.server = Server(sim, sim.sim_param.SERVICE_RATE)
        # self.user = User(sim, sim.sim_param.ARRIVAL_RATE)
        #######################################

        #######################################
        # TODO Task 2.3.1: and uncomment these lines
        #######################################
        self.servers = self.create_servers(sim, sim.sim_param.NUM_USERS, sim.sim_param.SERVICE_RATES)
        self.users = self.create_users(sim, sim.sim_param.NUM_USERS, sim.sim_param.ARRIVAL_RATES)
        #######################################

        # TODO Task 2.2.2: comment code below
        #######################################
        # self.buffer_content = 0
        
        ######################################

        #######################################
        # TODO Task 2.2.2: Rewrite code from above, your code goes here
        self.buffer = FiniteQueue() #buffer_size
        #######################################

    def reset(self):
        """
        Reset SysState object, including the generation of servers and users objects.
        """
        self.now = 0
        self.stop = False
        self.packets_dropped = 0
        self.packets_total = 0
        # TODO Task 2.3.1: comment these lines
        #######################################
        # self.server.reset(self.sim.sim_param.SERVICE_RATE)
        # self.user.reset(self.sim.sim_param.ARRIVAL_RATE)
        #######################################

        # TODO Task 2.3.1: and uncomment these lines
        #######################################
    
        if len(self.servers) == self.sim.sim_param.NUM_SERVERS:
            for i in range(self.sim.sim_param.NUM_SERVERS):
                self.servers[i].reset(self.sim.sim_param.SERVICE_RATES[i])
        else:
            self.servers = self.create_servers(self.sim, self.sim.sim_param.NUM_SERVERS, self.sim.sim_param.SERVICE_RATES)
        if len(self.users) == self.sim.sim_param.NUM_USERS:
            for i in range(self.sim.sim_param.NUM_USERS):
                self.users[i].reset(self.sim.sim_param.ARRIVAL_RATES[i])
        else:
            self.users = self.create_users(self.sim, self.sim.sim_param.NUM_USERS, self.sim.sim_param.ARRIVAL_RATES)
     
        #######################################

        # TODO Task 2.2.2: comment code below
        #######################################
        # self.buffer_content = 0
        
        #######################################

        #######################################
        # TODO Task 2.2.2: Rewrite code from above, your code goes here
        self.buffer = FiniteQueue(self.sim.sim_param.S) #S is the correct buffer max??
        pass
        #######################################

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

    def create_servers(self, sim: Simulation, num_servers: int, service_rates: list):
        """
        Create servers objects with appropriate parameters.
        :param sim: simulation object
        :param num_servers: number of servers defined in simparam
        :param service_rates: service rates of servers defined in simparam
        :return: list of num_servers server objects
        """
        #######################################
        # TODO Task 2.3.1: Your code goes here
        pass
        #######################################

    def create_users(self, sim: Simulation, num_users: int, arrival_rates: list):
        """
        Create users objects with appropriate parameters.
        :param sim: simulation object
        :param num_users: number of users defined in simparam
        :param arrival_rates: arrival rates of users defined in simparam
        :return: list of num_users user objects
        """
        #######################################
        # TODO Task 2.3.1: Your code goes here
        users = []
        for i in range(num_users):
            users.append(User(sim, arrival_rates[i]))
        return users
        pass
        #######################################

    def start_users(self):
        """
        Start generating packets by users
        """
        # TODO Task 2.3.2: comment code below
        ######################################
        # self.user.generate_packet_arrival()
        ######################################

        ######################################
        # TODO Task 2.3.2: Rewrite code from above, your code goes here
        for user in self.users:
            user.generate_packet_arrival()
        pass
        ######################################

    # TODO Task 2.2.2: Correct function declaration according to task description
    def add_packet_to_buffer(self, packet: Packet):
        """
        Attempt to add packet to buffer.
        :param packet: packet to be added to buffer
        :return: - True if could add packet to buffer, false if buffer is full
        """
        # TODO Task 2.2.2: comment code below
        #######################################
        # DONE Task 1.1.1:
        # Check if buffer is not full and add packet if it is the case
        # if self.buffer_content < self.sim.sim_param.S:
        #     self.buffer_content += 1
        #     return True
        #######################################

        #######################################
        # TODO Task 2.2.2: Rewrite code from above, your code goes here
        #######################################
        if not self.buffer.is_full():
            self.buffer.enqueue(packet)
            return True
        else:
            self.packet_dropped()
            return False

        #######################################
        # DONE Task 1.1.6:
        self.packet_dropped()
        return False
        #######################################

    # TODO Task 2.2.2: Correct function declaration according to task description
    def start_serving_packet(self, packet: Packet):
        """
        Attempt to start service of newly arrived packet.
        :param pkt_arrived: packet to be served
        :return: - False if server refuses to start service, true if successfully started service
        """
        #######################################
        # DONE Task 1.1.6:
        self.packet_entered()
        # TODO Task 2.3.3: comment code below
        #######################################
        # DONE Task 1.1.5:
        # Try to start service, note that the flag is set to true, as there is a new packet to be served
        # if self.server.start_service(pkt_arrived=True):
        #     return True
        # return False
        #######################################

        #######################################
        # TODO Task 2.3.3: Rewrite code from above, your code goes here
        self.packet_entered()

        for server in self.servers:
            if server.start_service(packet):
                return True
        return False
        #######################################



