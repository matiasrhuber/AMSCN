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

        #######################################
        # DONE Task 2.3.1:
        # TODO Task 3.1.4: Modify code below.
        self.servers = self.create_servers(sim, sim.sim_param.NUM_SERVERS, sim.sim_param.SERVICE_RATES, sim.sim_param.SERVERS_SEEDS)
        self.users = self.create_users(sim, sim.sim_param.NUM_USERS, sim.sim_param.ARRIVAL_RATES, sim.sim_param.USERS_SEEDS)
        
        #######################################

        #######################################
        # DONE Task 2.2.2:
        self.buffer = FiniteQueue(sim.sim_param.S)
        #######################################

        ######################################
        self.last_arrival = None
        ######################################


    def reset(self):
        """
        Reset SysState object, including the generation of servers and users objects.
        """
        self.now = 0
        self.stop = False
        self.packets_dropped = 0
        self.packets_total = 0

        # DONE Task 2.3.1:
        #######################################
        if len(self.servers) == self.sim.sim_param.NUM_SERVERS:
            for i in range(self.sim.sim_param.NUM_SERVERS):
                #######################################
                # TODO Task 3.1.4: Modify code below.
                self.servers[i].reset(self.sim.sim_param.SERVICE_RATES[i], self.sim.sim_param.SERVERS_SEEDS[i])
                
                #######################################
        else:
            #######################################
            # TODO Task 3.1.4: Modify code below.
            self.servers = self.create_servers(self.sim, self.sim.sim_param.NUM_SERVERS, self.sim.sim_param.SERVICE_RATES, self.sim.sim_param.SERVERS_SEEDS)
            #######################################
        if len(self.users) == self.sim.sim_param.NUM_USERS:
            for i in range(self.sim.sim_param.NUM_USERS):
                #######################################
                # TODO Task 3.1.4: Modify code below.
                self.users[i].reset(self.sim.sim_param.ARRIVAL_RATES[i], self.sim.sim_param.USERS_SEEDS)
                #######################################
        else:
            #######################################
            # TODO Task 3.1.4: Modify code below.
            self.users = self.create_users(self.sim, self.sim.sim_param.NUM_USERS, self.sim.sim_param.ARRIVAL_RATES, self.sim.sim_param.USERS_SEEDS)
            #######################################
        #######################################

        #######################################
        # DONE Task 2.2.2:
        self.buffer = FiniteQueue(self.sim.sim_param.S)
        #######################################

        self.last_arrival = None

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

    ######################################
    def count_arrival(self):
        """
        Process new arrival from some user. Count inter-arrival time and update the last arrival timestamp.
        """
        if self.last_arrival is not None:
            self.sim.statistics_collection.count_iat(self.now - self.last_arrival)
        self.last_arrival = self.now
    ######################################

    # TODO Task 3.1.4: Correct function declaration according to task description.
    def create_servers(self, sim: Simulation, num_servers: int, service_rates: list, seeds: list):
        """
        Create servers objects with appropriate parameters.
        :param sim: simulation object
        :param num_servers: number of servers defined in simparam
        :param service_rates: service rates of servers defined in simparam
        :return: list of num_servers server objects
        """
        #######################################
        # DONE Task 2.3.1:
        # initialize list of servers
        #######################################
        # TODO Task 3.1.4: Modify code below.
        servers = []
        for i in range(num_servers):
            seed = seeds[i] if i < len(seeds) else None
            servers.append(Server(sim, service_rates[i], seed))
        return servers
        #######################################

    # TODO Task 3.1.4: Correct function declaration according to task description.
    def create_users(self, sim: Simulation, num_users: int, arrival_rates: list, seeds: list):
        """
        Create users objects with appropriate parameters.
        :param sim: simulation object
        :param num_users: number of users defined in simparam
        :param arrival_rates: arrival rates of users defined in simparam
        :return: list of num_users user objects
        """
        #######################################
        # DONE Task 2.3.1:
        # initialize list of users
        #######################################
        # TODO Task 3.1.4: Modify code below.
        users = []
        for i in range(num_users):
            seed = seeds[i] if i < len(seeds) else None
            users.append(User(sim, arrival_rates[i], seed))
        return users
        #######################################

    def start_users(self):
        """
        Start generating packets by users
        """
        ######################################
        # DONE Task 2.3.2:
        for user in self.users:
            user.generate_packet_arrival()
        ######################################

    # DONE Task 2.2.2:
    def add_packet_to_buffer(self, packet: Packet):
        """
        Attempt to add packet to buffer.
        :param packet: packet to be added to buffer
        :return: - True if could add packet to buffer, false if buffer is full
        """

        #######################################
        # DONE Task 2.2.2:
        if self.buffer.add(packet):
            # packet is added to queue
            return True
        #######################################

        self.packet_dropped()
        return False


    # DONE Task 2.2.2:
    def start_serving_packet(self, pkt_arrived: Packet):
        """
        Attempt to start service of newly arrived packet.
        :param pkt_arrived: packet to be served
        :return: - False if server refuses to start service, true if successfully started service
        """
        self.packet_entered()

        #######################################
        # DONE Task 2.3.3:
        # try to add packet to service of one of the servers; return True as soon as could successfully add
        # or False if all servers are busy
        for server in self.servers:
            if server.start_service(pkt_arrived):
                return True
        return False
        #######################################



