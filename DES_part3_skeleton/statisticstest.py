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
        if self.dist_f == scipy.stats.norm:
            expected_freq = np.diff(self.dist_f.ppf([0, alpha], loc=mean, scale=var**0.5))
        elif self.dist_f == scipy.stats.expon:  
            expected_freq = np.diff(self.dist_f.ppf([0, alpha], loc=0, scale=1 / mean))
        
        # if frequencies are below 5 use neighbouring frequencies
        combined_emp_x = []
        combined_emp_n = []
        curr_freq_sum = 0
        for x, n in zip(self.emp_x, self.emp_n):
            if curr_freq_sum + n < 5:
                curr_freq_sum += n
            else:
                combined_emp_x.append(x)
                combined_emp_n.append(curr_freq_sum + n)
                curr_freq_sum = 0
            combined_emp_x.append(x)
            combined_emp_n.append(curr_freq_sum + n)
            self.emp_x = combined_emp_x
            self.emp_n = combined_emp_n
        
        observed_freq = self.emp_n
        print(expected_freq)
        chi_sq = np.sum((observed_freq - expected_freq)**2 / expected_freq)
        
        df = len(observed_freq) - est_parameters - 1
        
        critical_value = scipy.stats.chi2.ppf(1 - alpha, df)
        
        return chi_sq, critical_value
        #######################################



