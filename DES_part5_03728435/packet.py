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
        if self.t_arrival != other.t_arrival:
            return self.t_arrival < other.t_arrival
        else:
            return True

    def start_service(self, start_service_timestamp: float):
        """
        Change the status of the packet once the serving process starts.
        :param start_service_timestamp: the timestamp of the service start
        """
        self.waiting = False
        self.in_service = True
        self.t_start_service = start_service_timestamp

    def complete_service(self, complete_service_timestamp: float):
        """
        Change the status of the packet once the serving process is completed.
        :param complete_service_timestamp: the timestamp of the service completion
        """
        self.t_complete = complete_service_timestamp
        self.in_service = False
        self.completed = True

    def get_waiting_time(self):
        """
        Return the waiting time of the packet.
        :return: waiting time
        """
        if not self.in_service and not self.completed:
            raise SystemError("Packet has not been served yet.")
        else:
            return self.t_start_service - self.t_arrival

    def get_service_time(self):
        """
        Calculate and return the service time
        :return: service time
        """
        if not self.completed:
            raise SystemError("Packet is not completed yet.")
        else:
            return self.t_complete - self.t_start_service

    def get_system_time(self):
        """
        Calculate and return the system time (waiting time + service time)
        :return: system time (waiting time + serving time)
        """
        if not self.completed:
            raise SystemError("Packet is not completed yet.")
        else:
            return self.t_complete - self.t_arrival

    def get_inter_arrival_time(self):
        """
        Return the inter-arrival time of this packet from the previous packet generated by this user
        :return: inter-arrival time
        """
        return self.iat




