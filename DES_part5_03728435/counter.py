import numpy
import math
import scipy
import scipy.stats


class Counter(object):
    """
    Counter class is an abstract class, that counts values for statistics.

    Values are added to the internal array. The class is able to generate mean value, variance and standard deviation.
    The report function prints a string with name of the counter, mean value and variance.
    All other methods have to be implemented in subclasses.
    """

    def __init__(self, name="default"):
        """
        Initialize a counter with a name.
        The name is only for better distinction between counters.
        :param name: identifier for better distinction between various counters
        """
        self.name = name
        self.values = []

    def count(self, *args):
        """
        Count values and add them to the internal array.
        Abstract method - implement in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def reset(self, *args):
        """
        Delete all values stored in internal array.
        """
        self.values = []

    def get_mean(self):
        """
        Returns the mean value of the internal array.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def get_var(self):
        """
        Returns the variance of the internal array.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def get_stddev(self):
        """
        Returns the standard deviation of the internal array.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def report(self):
        """
        Print report for this counter.
        """
        if len(self.values) != 0:
            print("Name: " + str(self.name) + ", Mean: " + str(self.get_mean()) + ", Variance: " + str(self.get_var()))
        else:
            print("List for creating report is empty. Please check.")


class TimeIndependentCounter(Counter):
    """
    Counter for counting values independent of their duration.
    """

    def __init__(self, name="default"):
        """
        Initialize the TIC object.
        """
        super(TimeIndependentCounter, self).__init__(name)

    def count(self, value: float):
        """
        Add a new value to the internal array.
        :param: value that should be added to the internal array
        """
        self.values.append(value)

    def get_mean(self):
        """
        Return the mean value of the internal array.
        """
        if len(self.values) > 0:
            return numpy.mean(self.values)
        else:
            return None

    def get_var(self, biased=False):
        """
        Return the variance of the internal array.
        Note, that we take the estimated variance, not the exact variance.
        :param biased: bool indicating if the calculated variance should be biased
        """
        if biased:
            return numpy.var(self.values)
        else:
            return numpy.var(self.values, ddof=1)

    def get_stddev(self):
        """
        Returns the unbiased standard deviation of the internal array.
        """
        return numpy.sqrt(self.get_var())

    def report_confidence_interval(self, alpha: float = 0.05, print_report: bool = True):
        """
        Report a confidence interval with given significance level.
        This is implemented by using the t-table provided by scipy.
        :param alpha: the significance level (default: 5%)
        :param print_report: enables an output string
        :return: half width of the confidence interval
        """
        #######################################
        # TODO Task 5.1.1: Your code goes here
        if len(self.values) == 0:
            return None

        n = len(self.values)
        mean = self.get_mean()
        std_dev = self.get_stddev()

        # Calculate t critical value
        t_critical = scipy.stats.t.ppf(1 - alpha / 2, df=n-1)
        
        # Calculate half-width of the confidence interval
        half_width = t_critical * (std_dev / numpy.sqrt(n))

        if print_report:
            print(f"Name: {self.name}, Mean: {mean}, Confidence Interval: [{mean - half_width}, {mean + half_width}]")

        return half_width
        #######################################

    def is_in_confidence_interval(self, x: float, alpha: float = 0.05):
        """
        Check if sample x is in confidence interval with given significance level.
        :param x: is the sample
        :param alpha: is the significance level
        :return: true, if sample is in confidence interval
        """
        #######################################
        # TODO Task 5.1.1: Your code goes here
        if len(self.values) == 0:
            return False

        mean = self.get_mean()
        half_width = self.report_confidence_interval(alpha, print_report=False)

        lower_bound = mean - half_width
        upper_bound = mean + half_width

        return lower_bound <= x <= upper_bound
        #######################################

    def report_bootstrap_confidence_interval(self, alpha: float = 0.05, resample_size: int = 5000,
                                             print_report: bool = True):
        """
        Report bootstrapping confidence interval with given significance level.
        This is implemented with the bootstrap method. Hint: use numpy.random.choice for resampling
        :param alpha: significance level
        :param resample_size: resampling size
        :param print_report: enables an output string
        :return: lower and upper bound of confidence interval
        """
        #######################################
        # TODO Task 5.1.2: Your code goes here
        if len(self.values) == 0:
            return None

        original_mean = self.get_mean()
        n = len(self.values)

        bootstrapped_means = []
        for _ in range(resample_size):
            resample = numpy.random.choice(self.values, size=n, replace=True)
            bootstrapped_means.append(numpy.mean(resample))
        
        bootstrapped_means = numpy.array(bootstrapped_means)

        # Calculate bootstrap differences
        bootstrap_differences = bootstrapped_means - original_mean

        # Calculate the quantiles of the bootstrap differences
        lower_quantile = numpy.percentile(bootstrap_differences, (alpha / 2) * 100)
        upper_quantile = numpy.percentile(bootstrap_differences, (1 - alpha / 2) * 100)

        # Calculate the empirical bootstrap confidence interval
        lower_bound = original_mean - upper_quantile
        upper_bound = original_mean - lower_quantile

        if print_report:
            print(f"Name: {self.name}, Bootstrap Confidence Interval: [{lower_bound}, {upper_bound}]")

        return lower_bound, upper_bound

        #######################################

    def is_in_bootstrap_confidence_interval(self, x: float, resample_size: int = 5000, alpha: float = 0.05):
        """
        Check if sample x is in bootstrap confidence interval with given resample_size and significance level.
        :param x: is the sample
        :param resample_size: resample size
        :param alpha: is the significance level
        :return: true, if sample is in bootstrap confidence interval
        """
        #######################################
        # TODO Task 5.1.2: Your code goes here
        lower_bound, upper_bound = self.report_bootstrap_confidence_interval(alpha, resample_size, print_report=False)
        return lower_bound <= x <= upper_bound
        #######################################


class TimeDependentCounter(Counter):
    """
    Counter, that counts values considering their duration as well.

    Methods for calculating mean, variance and standard deviation are available.
    """

    def __init__(self, name="default"):
        """
        Initialize TDC with the simulation it belongs to and the name.
        :param: name is an identifier for better distinction between multiple counters.
        """
        super(TimeDependentCounter, self).__init__(name)
        self.first_timestamp = 0
        self.last_timestamp = 0
        self.weights = []

    def count(self, value: float, now: float):
        """
        Adds new value to internal array.
        Duration from last to current value is considered.
        :param value: value to be counted
        :param now: the timestamp when the value is counted
        """
        dt = now - self.last_timestamp
        if dt < 0:
            print("Error in calculating time dependent statistics. Current time is smaller than last timestamp.")
            raise ValueError
        self.values.append(value)
        self.weights.append(dt)
        self.last_timestamp = now

    def get_mean(self):
        """
        Return the mean value of the counter, normalized by the total duration of the simulation.
        """
        return float(sum([self.values[i] * self.weights[i] for i in range(len(self.values))])) /\
            float((self.last_timestamp - self.first_timestamp))

    def get_var(self):
        """
        Return the unbiased variance of the TDC.
        """
        dt = self.last_timestamp - self.first_timestamp
        mean = self.get_mean()
        return len(self.values) / (len(self.values) - 1) * (float(sum([self.values[i]**2 * self.weights[i]
                            for i in range(len(self.values))])) / float(dt) - mean**2)

    def get_stddev(self):
        """
        Returns the unbiased standard deviation of the internal array.
        """
        return numpy.sqrt(self.get_var())

    def reset(self):
        """
        Reset the counter to its initial state.
        """
        self.first_timestamp = 0
        self.last_timestamp = 0
        self.weights = []
        Counter.reset(self)


class TimeIndependentCrosscorrelationCounter(TimeIndependentCounter):
    """
    Counter that is able to calculate cross correlation (and covariance).
    """

    def __init__(self, name="default"):
        """
        Crosscorrelation counter contains three internal counters containing the variables
        :param name: is a string for better distinction between counters.
        """
        super(TimeIndependentCrosscorrelationCounter, self).__init__(name)
        #######################################
        # DONE Task 4.1.1:
        self.x = TimeIndependentCounter()
        self.y = TimeIndependentCounter()
        self.xy = TimeIndependentCounter()
        #######################################

    def reset(self):
        """
        Reset the TICCC to its initial state.
        """
        TimeIndependentCounter.reset(self)
        #######################################
        # DONE Task 4.1.1:
        self.x.reset()
        self.y.reset()
        self.xy.reset()
        #######################################

    def count(self, x, y):
        """
        Count two values and their product for the correlation between them. They are added to the two internal arrays.
        """
        #######################################
        # DONE Task 4.1.1:
        self.x.count(x)
        self.y.count(y)
        self.xy.count(x * y)
        #######################################

    def get_cov(self):
        """
        Calculate the covariance between the two internal arrays x and y.
        """
        #######################################
        # DONE Task 4.1.1:
        return self.xy.get_mean() - self.x.get_mean() * self.y.get_mean()
        #######################################

    def get_cor(self):
        """
        Calculate the correlation coefficient between the two internal arrays x and y.

        """
        #######################################
        # DONE Task 4.1.1:
        return self.get_cov() / math.sqrt(self.x.get_var() * self.y.get_var())
        #######################################

    def report(self):
        """
        Print a report string for the TICCC.
        """
        print('Name: ' + self.name + '; covariance = ' + str(self.get_cov()) + '; correlation = ' + str(self.get_cor()))


class TimeIndependentAutocorrelationCounter(TimeIndependentCounter):
    """
    Counter, that is able to calculate auto correlation with given lag.
    """

    def __init__(self, name="default", max_lag=10):
        """
        Create a new auto correlation counter object.
        :param name: string for better distinction between multiple counters
        :param max_lag: maximum available lag (defaults to 10)
        """
        super(TimeIndependentAutocorrelationCounter, self).__init__(name)
        #######################################
        # DONE Task 4.1.2:
        self.max_lag = max_lag
        #######################################

    def get_auto_cov(self, lag):
        """
        Calculate the auto covariance for a given lag.
        :return: auto covariance
        """
        #######################################
        # DONE Task 4.1.2:
        if lag <= self.max_lag:
            x = self.values
            y = self.values[-lag:] + self.values[:-lag]
            xy = []

            for i in range(len(x)):
                xy.append(x[i] * y[i])

            return numpy.mean(xy) - numpy.mean(x) * numpy.mean(y)

        else:
            raise RuntimeError("lag larger than max_lag, please correct!")
        #######################################

    def get_auto_cor(self, lag):
        """
        Calculate the auto correlation for a given lag.
        :return: auto correlation coefficient
        """
        #######################################
        # DONE Task 4.1.2:
        if lag <= self.max_lag:
            var = self.get_var()
            if var != 0:
                return self.get_auto_cov(lag) / var
            else:
                return 0.0
        else:
            raise RuntimeError("lag larger than max_lag, please correct!")
        #######################################

    def set_max_lag(self, max_lag):
        """
        Change maximum lag. Cycle length is set to max_lag + 1.
        """
        #######################################
        # DONE Task 4.1.2:
        self.max_lag = max_lag
        self.reset()
        #######################################

    def report(self):
        """
        Print report for auto correlation counter.
        """
        print('Name: ' + self.name)
        for i in range(0, self.max_lag + 1):
            print('Lag = ' + str(i) + '; covariance = ' + str(self.get_auto_cov(i)) + '; correlation = ' + str(
                self.get_auto_cor(i)))
