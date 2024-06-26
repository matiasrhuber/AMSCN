from matplotlib import pyplot as plt


class BoxPlot(object):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

    def __init__(self, name: str = "default"):
        """
        Constructor for a boxplot
        :param name: optional name of the statistics in boxplot
        """
        #######################################
        # TODO Task 2.5.1: Your code goes here
        self.name = name
        self.data = []
        #######################################

    def add_counter_data(self, values: list):
        """
        Add set of values of a counter to the internal array.
        :param values: list of values of a counter
        """
        #######################################
        # TODO Task 2.5.1: Your code goes here
        self.data.append(values)
        #######################################

    def plot(self, labels: list = None):
        """
        Plot function for boxplot.
        :param labels: if not None, it defines the labels for x-axis of boxplot
        """
        #######################################
        # TODO Task 2.5.1: Your code goes here
        plt.figure()
        plt.boxplot(self.data, labels=labels)
        plt.xlabel('Counter')
        plt.ylabel('Values')
        plt.title('Boxplot of {}'.format(self.name))
        plt.show()
        #######################################
