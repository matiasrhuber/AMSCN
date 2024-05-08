from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from user import User


class Packet(object):
    """
    Packet represents a data packet processed by the DES.

    It contains variables for measurements, which include timestamps (arrival, service start, service completion),
    the status of the packet (waiting, in service, completed) and the inter-arrival time of this packet.
    """

    def __init__(self, arrival_timestamp: float, user: User):
        """
        Initialize a packet with its arrival time and a User that has generated this packet.
        :param arrival_timestamp: timestamp of this packet arrival event
        :param user: user object this packet belongs to
        """
        self.user = user

        self.t_arrival = arrival_timestamp
        self.t_start_service = None
        self.t_complete = None

        self.waiting = True
        self.in_service = False
        self.completed = False

        self.iat = user.last_iat

    def __lt__(self, other):
        """
        Comparison is made by comparing arrival timestamps.
        """
        #######################################
        # TODO Task 2.1.1: Your code goes here
        pass
        #######################################

    def start_service(self, start_service_timestamp: float):
        """
        Change the status of the packet once the serving process starts.
        :param start_service_timestamp: the timestamp of the service start
        """
        #######################################
        # TODO Task 2.1.2: Your code goes here
        pass
        #######################################

    def complete_service(self, complete_service_timestamp: float):
        """
        Change the status of the packet once the serving process is completed.
        :param complete_service_timestamp: the timestamp of the service completion
        """
        #######################################
        # TODO Task 2.1.2: Your code goes here
        pass
        #######################################

    def get_waiting_time(self):
        """
        Return the waiting time of the packet.
        :return: waiting time
        """
        #######################################
        # TODO Task 2.1.2: Your code goes here
        pass
        #######################################

    def get_service_time(self):
        """
        Calculate and return the service time
        :return: service time
        """
        #######################################
        # TODO Task 2.1.2: Your code goes here
        pass
        #######################################

    def get_system_time(self):
        """
        Calculate and return the system time (waiting time + service time)
        :return: system time (waiting time + serving time)
        """
        #######################################
        # TODO Task 2.1.2: Your code goes here
        pass
        #######################################

    def get_inter_arrival_time(self):
        """
        Return the inter-arrival time of this packet from the previous packet generated by this user
        :return: inter-arrival time
        """
        #######################################
        # TODO Task 2.1.2: Your code goes here
        pass
        #######################################




