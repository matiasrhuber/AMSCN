import numpy


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

    def count(self, value):
        """
        Add a new value to the internal array.
        :param: value that should be added to the internal array
        """
        #######################################
        # TODO Task 2.4.1: Your code goes here
        pass
        #######################################

    def get_mean(self):
        """
        Return the mean value of the internal array.
        """
        #######################################
        # TODO Task 2.4.1: Your code goes here
        pass
        #######################################

    def get_var(self, biased=False):
        """
        Return the variance of the internal array.
        Note, that we take the estimated variance, not the exact variance.
        :param biased: bool indicating if the calculated variance should be biased
        """
        #######################################
        # TODO Task 2.4.1: Your code goes here
        pass
        #######################################

    def get_stddev(self):
        """
        Returns the unbiased standard deviation of the internal array.
        """
        #######################################
        # TODO Task 2.4.1: Your code goes here
        pass
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
        #######################################
        # TODO Task 2.4.2: Your code goes here
        pass
        #######################################

    def count(self, value: float, now: float):
        """
        Adds new value to internal array.
        Duration from last to current value is considered.
        :param value: value to be counted
        :param now: the timestamp when the value is counted
        """
        #######################################
        # TODO Task 2.4.2: Your code goes here
        pass
        #######################################

    def get_mean(self):
        """
        Return the mean value of the counter, normalized by the total duration of the simulation.
        """
        #######################################
        # TODO Task 2.4.2: Your code goes here
        pass
        #######################################

    def get_var(self):
        """
        Return the unbiased variance of the TDC.
        """
        #######################################
        # TODO Task 2.4.2: Your code goes here
        pass
        #######################################

    def get_stddev(self):
        """
        Returns the unbiased standard deviation of the internal array.
        """
        #######################################
        # TODO Task 2.4.2: Your code goes here
        pass
        #######################################

    def reset(self):
        """
        Reset the counter to its initial state.
        """
        #######################################
        # TODO Task 2.4.2: Your code goes here
        pass
        #######################################

