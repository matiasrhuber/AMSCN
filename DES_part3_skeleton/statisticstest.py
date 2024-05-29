import numpy
import scipy.stats
from enum import Enum

class TestDist(Enum):
    NORMAL = 1
    EXPONENTIAL = 2

class ChiSquare(object):

    def __init__(self, emp_x: list, emp_n: list, distr: TestDist = TestDist.NORMAL):
        """
        Initialize chi square test with observations and their frequency.
        :param emp_x: observation values (bins)
        :param emp_n: frequency
        :param distr: type of tested distribution
        """
        self.emp_x = emp_x
        self.emp_n = emp_n
        if distr == TestDist.NORMAL:
            self.dist_f = scipy.stats.norm
        if distr == TestDist.EXPONENTIAL:
            self.dist_f = scipy.stats.expon

    def test_distribution(self, alpha: float, mean: float, est_parameters: int = 0, var: float = None):
        """
        Test, if the observations fit into a given distribution.
        :param alpha: significance level of test
        :param mean: mean value of the tested distribution
        :param est_parameters: number of the distribution parameters estimated from samples
        :param var: variance value of the tested distribution if applicable
        :return: chi2-value and the corresponding table value
        """
        #######################################
        # TODO Task 3.7.1: Your code goes here.
        pass
        #######################################



