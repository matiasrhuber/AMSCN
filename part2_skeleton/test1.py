import unittest
from event import EventChain, PacketArrival, ServiceCompletion, SimulationTermination
from simulation import Simulation
import random
from simparam import SimParam
from user import User
from server import Server


class DESTest(unittest.TestCase):
    """
    This python unittest class checks the first part of the programming assignment for basic functionality.
    """

    # create default simulation setting for testing the methods
    sim = Simulation()

    def test_add_packet_to_buffer(self):
        """
        Test function add_packet_to_buffer. Add packets to queue and check for correct behavior.
        """
        DESTest.sim.reset()
        DESTest.sim.sim_param.S = 4
        s = DESTest.sim.sys_state

        self.assertEqual([True, 1], [s.add_packet_to_buffer(), s.buffer_content],
                         msg="Error in SysState. Should be able to add packet to a buffer. Buffer content should be 1")
        for i in range(DESTest.sim.sim_param.S - 1):
            self.assertEqual([True, i + 2], [s.add_packet_to_buffer(), s.buffer_content],
                             msg="Error in SysState. Could not add packet to queue.")
        self.assertEqual([False, DESTest.sim.sim_param.S], [s.add_packet_to_buffer(), s.buffer_content],
                         msg="Error in SysState. Could add packet to queue though it should be full.")

    def test_start_service(self):
        """
        Test function start_service of Server.
        """
        DESTest.sim.reset()
        DESTest.sim.sim_param.S = 4
        s = DESTest.sim.sys_state

        s.buffer_content = DESTest.sim.sim_param.S

        self.assertEqual(True, s.server.start_service(pkt_arrived=False),
                         msg="Error in Server. Should be able to start service of packet from buffer.")
        self.assertEqual([DESTest.sim.sim_param.S - 1, True], [s.buffer_content, s.server.server_busy],
                         msg="Error in Server. Wrong int indicates queue length, wrong bool server busy.")
        self.assertEqual(False, s.server.start_service(pkt_arrived=False),
                         msg="Error in Server. Should not be able to start service.")
        self.assertEqual(False, s.server.start_service(pkt_arrived=True),
                         msg="Error in Server. Should not be able to start service.")

        s.server.server_busy = False
        self.assertEqual([True, DESTest.sim.sim_param.S - 1], [s.server.start_service(pkt_arrived=True), s.buffer_content],
                         msg="Error in Sever. Should be able to start service of newly arrived packet, "
                             "buffer content should not change.")
        s.server.server_busy = False
        s.buffer_content = 0
        self.assertEqual([True, 0],
                         [s.server.start_service(pkt_arrived=True), s.buffer_content],
                         msg="Error in Server. Should be able to start service of newly arrived packet, "
                             "buffer content should not change.")

    def test_start_serving_packet(self):
        """
        Test function start_serving_packet of SysState.
        """
        DESTest.sim.reset()
        DESTest.sim.sim_param.S = 4
        s = DESTest.sim.sys_state

        self.assertEqual(True, s.start_serving_packet(),
                         msg="Error in SystemState. Should be able to start serving.")
        self.assertEqual(False, s.start_serving_packet(),
                         msg="Error in SystemState. Should not be able to start serving.")

    def test_packet_entered_dropped(self):
        """
        Test if functions packet_dropped() and packet_entered() are called correctly.
        """
        DESTest.sim.reset()
        DESTest.sim.sim_param.S = 4
        s = DESTest.sim.sys_state
        for _ in range(DESTest.sim.sim_param.S + 5):
            if not s.start_serving_packet():
                s.add_packet_to_buffer()
        s.server.complete_service()
        for _ in range(DESTest.sim.sim_param.S):
            s.server.start_service()
            s.server.complete_service()
        self.assertEqual([9, 4], [s.packets_total, s.packets_dropped],
                         msg="Error in SystemState. Wrong number of entered and dropped packets.")



    def test_event_chain(self):
        """
        Test module EventChain. Add and remove SimEvents and check the correct order.
        """
        # orders: SC = 0, CA = 1, ST = 2
        e = EventChain()
        ue = User(DESTest.sim, DESTest.sim.sim_param.ARRIVAL_RATE)
        server = Server(DESTest.sim, DESTest.sim.sim_param.SERVICE_RATE)
        e.insert(PacketArrival(None, 10, ue))
        e.insert(SimulationTermination(None, 10))
        e.insert(ServiceCompletion(None, 10, server))
        e.insert(PacketArrival(None, 5, ue))
        e.insert(ServiceCompletion(None, 2, server))
        results = [[2, 0], [5, 1], [10, 0], [10, 1], [10, 2]]
        self.assertEqual(5, len(e.event_list),
                         msg="Error in EventChain or SimEvent. EventChain should have 5 events.")

        for r in results:
            ev = e.remove_oldest_event()
            self.assertEqual(r, [ev.timestamp, ev.order],
                             msg="Error in EventChain or SimEvent. Events are sorted or returned in the wrong order.")

        self.assertEqual(0, len(e.event_list),
                         msg="Error in EventChain or SimEvent. EventChain should be empty.")

    def test_generate_packet_arrival(self):
        """
        Test packet arrival events generation of User.
        """
        DESTest.sim.reset()
        random.seed(0)
        ue = User(DESTest.sim, 0.1)
        results = [17, 15, 9, 6, 11]
        for r in results:
            ue.generate_packet_arrival()
            self.assertAlmostEqual(r, ue.last_iat, delta=1.0, msg="Error in User. Wrong sequence of inter-arrival times.")
        self.assertEqual(5, len(DESTest.sim.event_chain.event_list),
                         msg="Error in User. Wrong amount of events inserted.")

    def test_packet_arrival(self):
        """
        Test PacketArrival process function. Check, whether adding packets to server or queue or dropping them
        works correctly.
        """
        DESTest.sim.reset()
        DESTest.sim.sim_param.S = 1
        ue = DESTest.sim.sys_state.user
        self.assertEqual([0, False], [DESTest.sim.sys_state.buffer_content, DESTest.sim.sys_state.server.server_busy],
                         msg="Error in PacketArrival test. System initialization failed.")
        # first arrival should be served by the server, not enqueued
        PacketArrival(DESTest.sim, 0, ue).process()
        self.assertEqual([0, True], [DESTest.sim.sys_state.buffer_content, DESTest.sim.sys_state.server.server_busy],
                         msg="Error in PacketArrival. Packet has not been added to server.")

        self.assertEqual(2, len(DESTest.sim.event_chain.event_list),
                         msg="Error in PacketArrival. Wrong number of new SimEvents created in process function.")
        # second arrival should be enqueued
        PacketArrival(DESTest.sim, 0, ue).process()
        self.assertEqual([1, True], [DESTest.sim.sys_state.buffer_content, DESTest.sim.sys_state.server.server_busy],
                         msg="Error in PacketArrival. Packet should have been enqueued.")
        self.assertEqual(3, len(DESTest.sim.event_chain.event_list),
                         msg="Error in PacketArrival. Wrong number of new SimEvents created in process function.")
        # third ca should be dropped
        PacketArrival(DESTest.sim, 0, ue).process()
        self.assertEqual([1, True, 1], [DESTest.sim.sys_state.buffer_content, DESTest.sim.sys_state.server.server_busy,
                                        DESTest.sim.sys_state.packets_dropped],
                         msg="Error in PacketArrival. Packet should have been dropped.")
        self.assertEqual(4, len(DESTest.sim.event_chain.event_list),
                         msg="Error in PacketArrival. Wrong number of new SimEvents created in process function.")

    def test_generate_service_completion(self):
        """
        Test service completion events generation of Server.
        """
        DESTest.sim.reset()
        server = DESTest.sim.sys_state.server
        server.service_rate = 0.1
        for _ in range(10):
            server.generate_service_completion()
        self.assertEqual(10, len(DESTest.sim.event_chain.event_list),
                         msg="Error in User. Wrong amount of events inserted.")
        for _ in range(10):
            self.assertEqual(10, DESTest.sim.event_chain.remove_oldest_event().timestamp,
                             msg="Error in Server. Wrong service time.")

    def test_service_completion(self):
        """
        Test ServiceCompletion process function. Check, whether processing of service completion events works as
        desired (making server idle again or triggering new service start).
        """
        DESTest.sim.reset()
        server = DESTest.sim.sys_state.server
        server.server_busy = True
        DESTest.sim.sys_state.buffer_content = 1
        # first service completion should insert new service completion and take packet from queue
        ServiceCompletion(DESTest.sim, 0, server).process()
        self.assertEqual([0, True], [DESTest.sim.sys_state.buffer_content, DESTest.sim.sys_state.server.server_busy],
                         msg="Error in ServiceCompletion. Server should be busy and queue should be empty.")
        self.assertEqual(1, len(DESTest.sim.event_chain.event_list),
                         msg="Error in ServiceCompletion. Wrong number of new SimEvents created in process function.")

        # second service completion should make server idle again
        ServiceCompletion(DESTest.sim, 0, server).process()
        self.assertEqual([0, False], [DESTest.sim.sys_state.buffer_content, DESTest.sim.sys_state.server.server_busy],
                         msg="Error in ServiceCompletion. Server should be idle and queue should be empty.")
        self.assertEqual(1, len(DESTest.sim.event_chain.event_list),
                         msg="Error in ServiceCompletion. Wrong number of new SimEvents created in process function.")


    def test_do_simulation(self):
        """
        Test whole simulation with different seeds for the correct results. Simulation is reinitialized after every run.
        """
        DESTest.sim.sim_param = SimParam()
        DESTest.sim.sim_param.SERVICE_RATE = 0.0015
        DESTest.sim.sim_param.ARRIVAL_RATE = 0.002
        results = [38, 52, 50, 40, 47]
        for seed in range(5):
            DESTest.sim.reset()
            DESTest.sim.sim_param.SEED = seed
            random.seed(seed)
            DESTest.sim.do_simulation()
            self.assertEqual(results[seed], DESTest.sim.sys_state.packets_dropped,
                             msg="Error in Simulation. Wrong number of dropped packets for given seed.")


if __name__ == '__main__':
    unittest.main()
