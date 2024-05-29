import unittest
from simulation import Simulation
from packet import Packet
from counter import TimeIndependentCounter, TimeDependentCounter
import random
import numpy
from user import User
from server import Server


class DESTestExtended(unittest.TestCase):
    """
    This python unittest class checks the second part of the programming assignment for basic functionality.
    """

    # create default simulation setting for testing the methods
    sim = Simulation()

    def test_packets_comparison(self):
        user = User(DESTestExtended.sim, DESTestExtended.sim.sim_param.ARRIVAL_RATES[0])
        p1 = Packet(10, user)
        p2 = Packet(15, user)
        self.assertEqual(True, p1 < p2, msg="Error in overloading Packet class comparison operator, p1 should be smaller.")

    def test_packet(self):
        user = User(DESTestExtended.sim, DESTestExtended.sim.sim_param.ARRIVAL_RATES[0])
        user.last_iat = 1
        p1 = Packet(10, user)
        p1.start_service(18)
        p1.complete_service(21)
        self.assertEqual([8, 3, 11, 1], [p1.get_waiting_time(), p1.get_service_time(), p1.get_system_time(),
                                         p1.get_inter_arrival_time()], msg="Error in Packet class methods.")

    def test_finite_queue(self):
        """
        Test the basic behavior of the finite queue.
        """
        DESTestExtended.sim.sim_param.S = 3
        DESTestExtended.sim.reset()
        s = DESTestExtended.sim.sys_state
        self.assertEqual(True, s.buffer.is_empty(),
                         msg="Error in FiniteQueue. Wrong queue status after reset.")
        user = User(DESTestExtended.sim, DESTestExtended.sim.sim_param.ARRIVAL_RATES[0])
        p0 = Packet(0, user)
        self.assertEqual(True, s.buffer.add(p0), msg="Error in FiniteQueue. Should return true.")
        p1 = Packet(10, user)
        self.assertEqual(True, s.buffer.add(p1), msg="Error in FiniteQueue. Should return true.")
        p2 = Packet(5, user)
        self.assertEqual(True, s.buffer.add(p2), msg="Error in FiniteQueue. Should return true.")
        self.assertEqual(False, s.buffer.add(p1), msg="Error in FiniteQueue. Queue should be full.")
        self.assertEqual(3, s.buffer.get_queue_length(),
                         msg="Error in FiniteQueue. Wrong queue length.")
        self.assertEqual(p0, s.buffer.remove(), msg="Error in FiniteQueue. Wrong packet returned")
        self.assertEqual(2, s.buffer.get_queue_length(),
                         msg="Error in FiniteQueue. Wrong queue length.")
        self.assertEqual(p2, s.buffer.remove(), msg="Error in FiniteQueue. Wrong packet returned")
        s.buffer.flush()
        self.assertEqual(True, s.buffer.is_empty(), msg="Error in FiniteQueue. Wrong state after flush")

    def test_packets_queue_integration(self):
        DESTestExtended.sim.sim_param.S = 3
        DESTestExtended.sim.reset()
        user = User(DESTestExtended.sim, DESTestExtended.sim.sim_param.ARRIVAL_RATES[0])
        user.last_iat = 0
        p1 = user.generate_packet()
        user.generate_packet_arrival()
        self.assertEqual(1, len(DESTestExtended.sim.event_chain.event_list), msg="Error in User. Should be 1 event")
        server = Server(DESTestExtended.sim, DESTestExtended.sim.sim_param.SERVICE_RATES[0])
        self.assertEqual([True, p1, True, True],
                         [server.start_service(p1), server.packet_in_service, server.server_busy, p1.in_service],
                         msg="Error in Server. Should start service of given packet")
        p2 = user.generate_packet()
        user.generate_packet_arrival()
        self.assertEqual(False, server.start_service(p2),
                         msg="Error in Server. Should not be able to start service")
        self.assertEqual(True, DESTestExtended.sim.sys_state.add_packet_to_buffer(p2),
                         msg="Error in SysState. Should be able to add packet to buffer")
        self.assertEqual([False, False, True, True, False, False], [p1.waiting, p1.completed, p1.in_service,
                                                                    p2.waiting, p2.completed, p2.in_service],
                                                                    msg="Error in Packet. Wrong status.")
        self.assertEqual(p2, DESTestExtended.sim.sys_state.buffer.remove(),
                         msg="Error in SysState. Wrong packet returned from buffer")
        server.complete_service()
        self.assertEqual([False, True, False, None], [p1.waiting, p1.completed, p1.in_service, server.packet_in_service],
                         msg="Error in Packet. Wrong status.")

    def test_multiple_servers_users(self):
        DESTestExtended.sim.sim_param.NUM_USERS = 3
        DESTestExtended.sim.sim_param.ARRIVAL_RATES = [0.001, 0.001, 0.001]

        DESTestExtended.sim.sim_param.NUM_SERVERS = 2
        DESTestExtended.sim.sim_param.SERVICE_RATES = [0.0001, 0.0001]

        DESTestExtended.sim.reset()

        self.assertEqual([3, 2], [len(DESTestExtended.sim.sys_state.users),
                                  len(DESTestExtended.sim.sys_state.servers)],
                         msg="Error in SysState. Wrong number of servers or users.")

        DESTestExtended.sim.sys_state.start_users()

        self.assertEqual(3, len(DESTestExtended.sim.event_chain.event_list),
                         msg="Error in SystemState. Wrong number of events for 2 users.")

        user = DESTestExtended.sim.sys_state.users[0]
        user.last_iat = 0
        DESTestExtended.sim.event_chain.remove_oldest_event().process()

        self.assertEqual(4, len(DESTestExtended.sim.event_chain.event_list),
                         msg="Error in SystemState. Wrong number of events after processing.")
        self.assertEqual([True, False], [DESTestExtended.sim.sys_state.servers[0].server_busy,
                                         DESTestExtended.sim.sys_state.servers[1].server_busy],
                         msg="Error in SysState. Wrong servers' statuses")
        DESTestExtended.sim.event_chain.remove_oldest_event().process()
        self.assertEqual(5, len(DESTestExtended.sim.event_chain.event_list),
                         msg="Error in SystemState. Wrong number of events after processing.")
        self.assertEqual([True, True], [DESTestExtended.sim.sys_state.servers[0].server_busy,
                                        DESTestExtended.sim.sys_state.servers[1].server_busy],
                         msg="Error in SysState. Wrong servers' statuses")
        DESTestExtended.sim.event_chain.remove_oldest_event().process()
        self.assertEqual(5, len(DESTestExtended.sim.event_chain.event_list),
                         msg="Error in SystemState. Wrong number of events after processing.")

        self.assertEqual(1, DESTestExtended.sim.sys_state.buffer.get_queue_length(),
                         msg="Error in FiniteQueue. Wrong queue length.")

    def test_TIC(self):
        """
        Test the TimeIndependentCounter
        """
        tic = TimeIndependentCounter()
        tic.count(3)
        tic.count(2)
        tic.count(5)
        tic.count(0)
        self.assertEqual(2.5, tic.get_mean(),
                         msg="Error in TimeIndependentCounter. Wrong mean calculation or wrong counting.")
        self.assertEqual(numpy.var([3, 2, 5, 0], ddof=1), tic.get_var(),
                         msg="Error in TimeIndependentCounter. Wrong variance calculation or wrong counting.")
        self.assertEqual(numpy.std([3, 2, 5, 0], ddof=1), tic.get_stddev(),
                         msg="Error in TimeIndependentCounter. Wrong std dev calculation or wrong counting.")
        tic.reset()
        tic.count(3.)
        tic.count(2.)
        tic.count(5.)
        tic.count(0.)
        self.assertEqual(2.5, tic.get_mean(),
                         msg="Error in TimeIndependentCounter. Wrong mean calculation or wrong counting.")
        self.assertEqual(numpy.var([3, 2, 5, 0], ddof=1), tic.get_var(),
                         msg="Error in TimeIndependentCounter. Wrong variance calculation or wrong counting.")
        self.assertEqual(numpy.std([3, 2, 5, 0], ddof=1), tic.get_stddev(),
                         msg="Error in TimeIndependentCounter. Wrong std dev calculation or wrong counting.")

    def test_TDC(self):
        """
        Test the TimeDependentCounter
        """
        tdc = TimeDependentCounter()
        tdc.count(5, 2)
        tdc.count(10, 6)
        tdc.count(0, 8)
        tdc.count(10, 10)
        self.assertEqual(7.0, tdc.get_mean(),
                         msg="Error in TimeDependentCounter. Wrong mean calculation or wrong counting.")
        self.assertEqual(16.0*4/3, tdc.get_var(),
                         msg="Error in TimeDependentCounter. Wrong variance calculation or wrong counting.")
        self.assertEqual((16.0*4/3)**0.5, tdc.get_stddev(),
                         msg="Error in TimeDependentCounter. Wrong std dev calculation or wrong counting.")

    def test_do_simulation(self):
        """
        Test whole simulation with different seeds for the correct results. Simulation is reinitialized after every run.
        """
        DESTestExtended.sim.sim_param.NUM_USERS = 3
        DESTestExtended.sim.sim_param.ARRIVAL_RATES = [0.001, 0.001, 0.001]

        DESTestExtended.sim.sim_param.NUM_SERVERS = 2
        DESTestExtended.sim.sim_param.SERVICE_RATES = [0.0015, 0.0015]
        results = [14, 15, 19, 12, 17]
        for seed in range(5):
            DESTestExtended.sim.reset()
            DESTestExtended.sim.sim_param.SEED = seed
            random.seed(seed)
            self.assertEqual(results[seed], DESTestExtended.sim.do_simulation().packets_dropped,
                             msg="Error in Simulation. Wrong number of dropped packets for given seed.")

        self.assertLess(len(DESTestExtended.sim.statistics_collection.cnt_wt.values), 300,
                        msg="Error in Simulation. Should count less than 300 values for waiting time.")
        self.assertGreater(len(DESTestExtended.sim.statistics_collection.cnt_wt.values), 250,
                           msg="Error in Simulation. Should count more than 250 values for waiting time.")
        self.assertGreater(len(DESTestExtended.sim.statistics_collection.cnt_ql.values), 5,
                           msg="Error in Simulation. Should count more than 5 values for queue length.")
        self.assertGreater(DESTestExtended.sim.statistics_collection.cnt_ql.get_mean(), 1,
                           msg="Error in Simulation. Mean queue length should be more than one.")
        self.assertLess(DESTestExtended.sim.statistics_collection.cnt_ql.get_mean(), 2,
                        msg="Error in Simulation. Mean queue length should be less then two.")
        self.assertLess(DESTestExtended.sim.statistics_collection.cnt_bs.get_mean(), 2,
                        msg="Error in Simulation. Should be less than two busy servers on average.")
        self.assertGreater(DESTestExtended.sim.statistics_collection.cnt_bs.get_mean(), 1,
                           msg="Error in Simulation. Should be more than one busy servers on average.")


if __name__ == '__main__':
    unittest.main()
