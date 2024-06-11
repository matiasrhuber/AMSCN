import unittest
from simulation import Simulation
from rns import UniformRNS
import numpy as np
from statisticstest import ChiSquare, TestDist
from simparam import ARR_PROCESS
from matplotlib import pyplot

class DESTest(unittest.TestCase):
    """
    This python unittest class checks the third part of the programming assignment for basic functionality.
    """

    # create default simulation setting for testing the methods
    sim = Simulation()

    def test_uniform_rns(self):
        uniform_rns = UniformRNS(10,20)
        samples = []
        for _ in range(100000):
            samples.append(uniform_rns.next())
        self.assertGreater(min(samples), 10, msg="Error in UniformRNS. Samples can not be smaller than 10")
        self.assertGreater(20, max(samples), msg="Error in UniformRNS. Samples can not be greater than 20")
        self.assertAlmostEqual(15, np.mean(samples), delta=0.1, msg="Error in UniformRNS. Wrong mean.")

    def test_single_user_server_rns(self):
        """
        Test the basic implementation of rho and the system utilization.
        """
        DESTest.sim.sim_param.SIM_TIME = 100000000
        DESTest.sim.sim_param.S = 10000
        DESTest.sim.sim_param.NUM_USERS = 1
        DESTest.sim.sim_param.NUM_SERVERS = 1
        DESTest.sim.sim_param.USERS_SEEDS = [0]
        DESTest.sim.sim_param.SERVERS_SEEDS = [1]
        DESTest.sim.sim_param.USERS_ARRIVAL_PROCESS = ARR_PROCESS.EXPONENTIAL
        for mu in [0.001 / 0.5, 0.001 / 0.9, 0.001 / 0.8, 0.001 / 0.01]:
            DESTest.sim.sim_param.SERVICE_RATES = [mu]
            DESTest.sim.sim_param.ARRIVAL_RATES = [0.001]
            DESTest.sim.reset()
            r = DESTest.sim.do_simulation().mean_number_busy_servers
            self.assertAlmostEqual(1 / mu * 0.001, r, delta=1 / mu * 0.001 * .2,
                                   msg="Error in RNS or CounterCollection. Should have gotten a different value for" + \
                                       " the system utilization with given rho.")

    def test_multiple_user_server_rns(self):
        """
        Test the basic implementation of rho and the system utilization.
        """
        DESTest.sim.sim_param.SIM_TIME = 100000000
        DESTest.sim.sim_param.S = 100000
        DESTest.sim.sim_param.SERVERS_SEEDS = [1]
        DESTest.sim.sim_param.USERS_SEEDS = [0, 1]
        DESTest.sim.sim_param.NUM_USERS = 2
        DESTest.sim.sim_param.NUM_SERVERS = 1
        DESTest.sim.sim_param.USERS_ARRIVAL_PROCESS = ARR_PROCESS.EXPONENTIAL

        for lam in [0.001 * 0.002, 0.2 * 0.002, 0.4 * 0.002, 0.45 * 0.002]:  # 0.001/0.01,
            DESTest.sim.sim_param.ARRIVAL_RATES = [lam, lam]
            DESTest.sim.sim_param.SERVICE_RATES = [0.002]
            DESTest.sim.reset()

            r = DESTest.sim.do_simulation().mean_number_busy_servers
            self.assertAlmostEqual(r, lam / 0.002 * 2, delta=lam / 0.002 * 2 * .2,
                                   msg="Error in RNS or CounterCollection. Should have gotten a different value for" + \
                                       " the system utilization with given rho.")

        DESTest.sim.sim_param.SIM_TIME = 100000000
        DESTest.sim.sim_param.S = 100000
        DESTest.sim.sim_param.SERVERS_SEEDS = [0, 1]
        DESTest.sim.sim_param.USERS_SEEDS = [0]
        DESTest.sim.sim_param.NUM_USERS = 1
        DESTest.sim.sim_param.NUM_SERVERS = 2

        for mu in [0.001 / 0.2, 0.001 / 0.5, 0.001 / 0.8, 0.001 / 0.01]:
            DESTest.sim.sim_param.SERVICE_RATES = [mu, mu]
            DESTest.sim.sim_param.ARRIVAL_RATES = [0.001]
            DESTest.sim.reset()
            r = DESTest.sim.do_simulation().mean_number_busy_servers
            self.assertAlmostEqual(r, 1 / mu * 0.001, delta=1 / mu * 0.001 * .2,
                                   msg="Error in RNS or CounterCollection. Should have gotten a different value for" + \
                                       " the system utilization with given rho.")

    def test_chi_square_normal(self):
        """
        This task is used to verify the implementation of the chi square test.
        First, 1000 samples are drawn from a normal distribution. Afterwards the chi square test is run on them to see,
        whether they follow the original or another given distribution.
        """
        alpha = .1
        values = []
        values2 = []
        np.random.seed(0)
        for _ in range(1000):
            values.append(np.random.normal(5, 1))
            values2.append(np.random.uniform(0, 10))

        emp_n, emp_x = np.histogram(values, bins=20, range=(0, 10))

        cs = ChiSquare(emp_n=emp_n, emp_x=emp_x, distr=TestDist.NORMAL)

        [c1, c2] = cs.test_distribution(alpha, 5, var=1)

        self.assertGreater(c2, c1, msg="Error in Chi Square Test. Hypothesis should not be rejected.")

        emp_n, emp_x = np.histogram(values2, bins=20, range=(0, 10))

        cs = ChiSquare(emp_n=emp_n, emp_x=emp_x, distr=TestDist.NORMAL)

        [c1, c2] = cs.test_distribution(alpha, 5, var=1)

        self.assertGreater(c1, c2, msg="Error in Chi Square Test. Hypothesis should be rejected.")

    def test_chi_square_exp(self):
        """
        This task is used to verify the implementation of the chi square test.
        First, 1000 samples are drawn from an exponential distribution. Afterwards the chi square test is run on them to see,
        whether they follow the original or another given distribution.
        """
        alpha = .1
        values = []
        values2 = []
        np.random.seed(0)
        for _ in range(1000):
            values.append(np.random.exponential(50, 1))
            values2.append(np.random.exponential(1000, 1))

        emp_n, emp_x = np.histogram(values, bins=30, range=(0, 200))

        cs = ChiSquare(emp_n=emp_n, emp_x=emp_x, distr=TestDist.EXPONENTIAL)

        [c1, c2] = cs.test_distribution(alpha, 50, est_parameters=1)


        self.assertGreater(c2, c1, msg="Error in Chi Square Test. Hypothesis should not be rejected.")

        emp_n, emp_x = np.histogram(values2, bins=30, range=(0, 5000))

        cs = ChiSquare(emp_n=emp_n, emp_x=emp_x, distr=TestDist.EXPONENTIAL)

        [c1, c2] = cs.test_distribution(alpha, 1000, est_parameters=1)

        self.assertGreater(c1, c2, msg="Error in Chi Square Test. Hypothesis should be rejected.")


if __name__ == '__main__':
    unittest.main()
