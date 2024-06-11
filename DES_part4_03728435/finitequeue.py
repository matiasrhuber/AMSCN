from queue import PriorityQueue
from packet import Packet


class FiniteQueue(object):
    """
    Class representing a finite queue with the system buffer.

    It is a priority queue with finite capacity. Methods contain adding and removing packets
    as well as checking the current number of packets in the buffer. Clearing the queue is implemented with the method flush.
    """

    def __init__(self, max_size: int):
        """
        Initialize the finite queue
        :param max_size: buffer spaces in queue
        :return: FiniteQueue object
        """
        self.buffer = PriorityQueue(maxsize=max_size)

    def add(self, packet: Packet):
        """
        Try to add a packet to the queue
        :param packet: packet which is supposed to be queued
        :return: true if packet has been enqueued, false if rejected
        """
        try:
            self.buffer.put_nowait(packet)
            return True
        except:
            return False

    def remove(self):
        """
        Pull the smallest packet from buffer and return it
        :return: the smallest packet
        """
        try:
            return self.buffer.get_nowait()
        except:
            return None

    def get_queue_length(self):
        """
        :return: current number of packets in the queue
        """
        return self.buffer.qsize()

    def is_empty(self):
        """
        :return: true if queue is empty
        """
        return self.buffer.empty()

    def flush(self):
        """
        erase all packets from the buffer
        """
        while not self.is_empty():
            try:
                self.remove()
            except:
                continue
