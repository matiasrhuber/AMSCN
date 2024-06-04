import numpy as np
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
        # Expected frequencies

        dist = scipy.stats.expon
        orig_ppf = dist.cdf(self.emp_x, loc=0, scale=50)
        orig_ppf = np.diff(np.append(orig_ppf,[1]))

        quantiles = []
        freq = []
        new_val = 0
        ppf = []
        new_ppf = 0

        for i,val in enumerate(self.emp_n):
            if (val > 5) & (new_val == 0):
                freq.append(val)
                quantiles.append(self.emp_x[i])
                ppf.append(orig_ppf[i])
                continue
            new_val += val
            new_ppf += orig_ppf[i]
            if new_val > 5:
                freq.append(new_val)
                quantiles.append(self.emp_x[i])
                ppf.append(new_ppf)
                new_val = 0
                new_ppf = 0
                continue

        expected_freq = np.multiply(np.array(ppf),np.sum(freq))
        chi_sq = np.sum((freq - expected_freq)**2 / expected_freq)
        df = len(self.emp_n) - est_parameters - 1
        critical_value = scipy.stats.chi2.ppf(1 - alpha, df)

       
        return chi_sq, critical_value
        #######################################



