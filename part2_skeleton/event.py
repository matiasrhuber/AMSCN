from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from simulation import Simulation
    from user import User
    from server import Server
import heapq


class EventChain(object):
    """
    This class contains a queue of events.

    Events can be inserted and removed from queue and are sorted by their time and order.
    Always the oldest event with the smallest order is removed.
    """

    def __init__(self):
        """
        Initialize event chain
        """
        self.event_list = []

    def insert(self, e: SimEvent):
        """
        Inserts event e to the event chain. Event chain is sorted during insertion.
        :param: e is of type SimEvent
        """
        #######################################
        # DONE Task 1.2.2:
        heapq.heappush(self.event_list, e)
        #######################################

    def remove_oldest_event(self):
        """
        Remove event with smallest timestamp (and order) from event chain
        :return: next event in event chain
        """
        #######################################
        # DONE Task 1.2.2:
        return heapq.heappop(self.event_list)
        #######################################


class SimEvent(object):
    """
    SimEvent represents an abstract type of simulation event.

    Contains mainly abstract methods that should be implemented in the subclasses.
    Comparison for insertion into EventChain is implemented by comparing first the timestamps and then the orders
    """

    def __init__(self, sim: Simulation, timestamp: float):
        """
        Initialization routine, setting the timestamp of the event and the simulation it belongs to.
        :param sim: simulation object the event belongs to
        :param timestamp: timestamp of the event execution
        """
        self.timestamp = timestamp
        self.sim = sim
        self.order = 0

    def process(self):
        """
        General event processing routine. Should be implemented in subclass.
        """
        raise NotImplementedError("Please Implement method \"process\" in subclass of SimEvent")

    def __lt__(self, other):
        """
        Comparison is made by comparing timestamps. If time stamps are equal, orders are compared.
        """
        #######################################
        # DONE Task 1.2.1:
        if self.timestamp != other.timestamp:
            return self.timestamp < other.timestamp
        elif self.order != other.order:
            return self.order < other.order
        else:
            return True
        #######################################


class PacketArrival(SimEvent):
    """
    Defines a new packet arrival event
    """

    def __init__(self, sim: Simulation, timestamp: float, user: User):
        """
        Create a new packet arrival event with a given execution time (when arrival should happen).
        Order of packet arrival event is set to 1 (second highest).
        :param user: user that generates a packet
        """
        super(PacketArrival, self).__init__(sim, timestamp)
        self.user = user
        self.order = 1

    def process(self):
        """
        Processing procedure of a packet arrival.
        """
        #######################################
        # TODO Task 2.2.3: Comment code below
        #######################################
        # DONE Task 1.3.2:
        # generate next packet arrival event for this user
        self.user.generate_packet_arrival()
        # try to start service; if server is busy, add to buffer
        if not self.sim.sys_state.start_serving_packet():
            self.sim.sys_state.add_packet_to_buffer()
        #######################################

        #######################################
        # TODO Task 2.2.3: Rewrite code from above, your code goes here
        pass
        #######################################


class ServiceCompletion(SimEvent):
    """
    Defines a service completion event (highest order in EventChain)
    """

    def __init__(self, sim: Simulation, timestamp: float, server: Server):
        """
        Create a new service completion event with given execution time (when service is being finished).
        Order of service completion event is set to 0 (highest).
        :param server: server that performs service
        """
        super(ServiceCompletion, self).__init__(sim, timestamp)
        self.server = server
        self.order = 0

    def process(self):
        """
        Processing procedure of a service completion.
        """
        #######################################
        # DONE Task 1.3.4:
        # Free up the server.
        self.server.complete_service()
        # Start serving the next packet from buffer if buffer is not empty.
        self.server.start_service()
        #######################################


class SimulationTermination(SimEvent):
    """
    Defines the end of a simulation. (least order in EventChain)
    """

    def __init__(self, sim, timestamp):
        """
        Create a new simulation termination event with given execution time.
        Order of simulation termination event is set to 2 (lowest)
        """
        super(SimulationTermination, self).__init__(sim, timestamp)
        self.order = 2

    def process(self):
        """
        Simulation stop flag is set to true, so simulation is stopped after this event.
        """
        #######################################
        # DONE Task 1.3.5:
        self.sim.sys_state.stop = True
        #######################################
