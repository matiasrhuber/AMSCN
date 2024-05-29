import math
from random import Random


class RNS(object):
    """
    Basic abstract class for random number streams.

    To be implemented in subclass.
    Contains a Random class r in order to allow different seeds for different RNS
    """

    def __init__(self, the_seed: float=None):
        """
        Initialize the general RNS with an optional seed.
        All further initialization is in subclasses.
        """
        self.r = Random(the_seed)

    def set_parameters(self, *args):
        NotImplementedError("Implement in subclass")

    def next(self):
        """
        Method should be overwritten in subclass.
        """
        return 0


class ExponentialRNS(RNS):
    """
    Class to provide exponentially distributed random numbers. After initialization, new numbers can be generated
    using next(). Initialization with given lambda and optional seed.
    :param lambda_x: the mean of the exponential distribution (in ms)
    :param the_seed: optional seed for the random number stream
    """

    def __init__(self, lambda_x : float, the_seed: float=None):
        """
        Initialize Exponential RNS and set the parameters (mean).
        :param lambda_x: the rate of the corresponding Poisson distribution [pkt/ms]
        :param the_seed: optional seed for the random number stream
        """
        super(ExponentialRNS, self).__init__(the_seed)
        #######################################
        # TODO Task 3.1.1: Your code goes here.
        pass
        #######################################

    def set_parameters(self, lambda_x: float):
        """
        Set parameter lambda, hence the mean of the exponential distribution.
        :param lambda_x: the rate of the corresponding Poisson distribution [pkt/ms]
        """
        #######################################
        # TODO Task 3.1.1: Your code goes here.
        pass
        #######################################

    def next(self):
        """
        Generate the next random number using the inverse transform method.
        """
        #######################################
        # TODO Task 3.1.1: Your code goes here.
        pass
        #######################################


class UniformRNS(RNS):
    """
    Class to provide uniformly distributed random numbers. After initialization, new numbers can be generated
    using next(). Initialization with upper and lower bound and optional seed.
    :param a: the lower bound of the uniform distribution
    :param b: the upper bound of the uniform distribution
    :param the_seed: optional seed for the random number stream
    """

    def __init__(self, a: float, b: float, the_seed=None):
        """
        Initialize Uniform RNS and set the parameters.
        :param a: lower bound
        :param b: upper bound
        :param the_seed: optimal seed
        """
        super(UniformRNS, self).__init__(the_seed)
        #######################################
        # TODO Task 3.1.1: Your code goes here.
        pass
        #######################################

    def set_parameters(self, a, b):
        """
        Set parameters a and b, the upper and lower bound of the distribution
        :param a: lower bound
        :param b: upper bound
        """
        #######################################
        # TODO Task 3.1.1: Your code goes here.
        pass
        #######################################

    def next(self):
        """
        Generate the next random number using the inverse transform method.
        """
        #######################################
        # TODO Task 3.1.1: Your code goes here.
        pass
        #######################################
