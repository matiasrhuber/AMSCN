import numpy
import scipy.stats
from enum import Enum


class TestDist(Enum):
    NORMAL = 1
    EXPONENTIAL = 2


class ChiSquare(object):

    def __init__(self, emp_x, emp_n, distr: TestDist=TestDist.NORMAL):
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

    def test_distribution(self, alpha, mean, est_parameters=0, var=None):
        """
        Test, if the observations fit into a given distribution.
        :param alpha: significance level of test
        :param mean: mean value of the tested distribution
        :param est_parameters: number of the distribution parameters estimated from samples
        :param var: variance value of the tested distribution if applicable
        :return: chi2-value and the corresponding table value
        """
        #######################################
        # DONE Task 3.7.1:
        o_i, bins = [self.emp_n, self.emp_x]
        n = numpy.sum(self.emp_n)
        e_i = []
        chi2 = 0.
        if var is None:
            dist = self.dist_f(scale=mean)
        else:
            dist = self.dist_f(mean, numpy.sqrt(var))

        for i in range(len(bins) - 1):
            e_i.append(n * (dist.cdf(bins[i + 1]) - dist.cdf(bins[i])))
        if max(e_i) < 5.0:
            raise ValueError("Not possible to test given data with Chi-square.")
        # Starting interval combination, min Ei=5
        init_length = len(e_i)
        o_i_combined = []
        e_i_combined = []

        o_i_head_sums = []
        e_i_head_sums = []

        k = 0
        k_head = 0
        while e_i[k_head] < 5.0:
            head_sum = 0.0
            while k < init_length:
                head_sum += e_i[k]
                if head_sum < 5.0:
                    k += 1
                else:
                    break
            e_i_head_sums.append(head_sum)
            o_i_head_sum = 0.0
            for kk in range(k_head, k + 1):
                o_i_head_sum += o_i[kk]
            k_head = k + 1
            k = k + 1
            o_i_head_sums.append(o_i_head_sum)

        k = init_length - 1
        k_tail = init_length - 1
        o_i_tail_sums = []
        e_i_tail_sums = []
        while e_i[k_tail] < 5.0:
            tail_sum = 0.0
            while k > 0:
                tail_sum += e_i[k]
                if tail_sum < 5.0:
                    k -= 1
                else:
                    break
            e_i_tail_sums.append(tail_sum)
            o_i_tail_sum = 0.0
            for kk in range(k, k_tail):
                o_i_tail_sum += o_i[kk]
            k_tail = k - 1
            k = k - 1
            o_i_tail_sums.append(o_i_tail_sum)

        # Formulate the combined intervals
        # The left tail - head
        for i in range(len(o_i_head_sums)):
            o_i_combined.append(o_i_head_sums[i])
            e_i_combined.append(e_i_head_sums[i])
        # The intermediate intervals stay
        for kk in range(k_head, k_tail + 1):
            o_i_combined.append(o_i[kk])
            e_i_combined.append(e_i[kk])
        # The right tail - tail
        for i in range(len(o_i_tail_sums)-1, -1, -1):
            o_i_combined.append(o_i_tail_sums[i])
            e_i_combined.append(e_i_tail_sums[i])

        for k in range(len(e_i_combined)):
            d = o_i_combined[k] - e_i_combined[k]
            if e_i_combined[k] != 0:
                chi2 += d * d / e_i_combined[k]
            else:
                print('Error: Division by zero in ChiSquare calculation!')

        # degrees of freedom: k-s-1
        # s - number of estimated by samples statistics
        chi2_table = scipy.stats.chi2.ppf(1 - alpha, len(e_i_combined) - 1 - est_parameters)

        print('Mean: ' + str(mean) + ', var: ' + str(var) + ', chi2: ' \
              + str(chi2) + '; ' + str((1 - alpha) * 100) + '%-quantile: ' + str(chi2_table))

        if chi2 > chi2_table:
            print("hypothesis rejected, the samples don't follow the distribution.")
        else:
            print("hypothesis not rejected, the samples follow the distribution.")

        return [chi2, chi2_table]
        #######################################



