from matplotlib import pyplot
from enum import Enum
import numpy as np



class BoxPlot(object):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

    def __init__(self, name: str = "default"):
        """
        Constructor for a boxplot
        :param name: optional name of the statistics in boxplot
        """
        self.counters_values = []
        self.name = name

    def add_counter_data(self, values: list):
        """
        Add set of values of a counter to the internal array.
        :param values: list of values of a counter
        """
        self.counters_values.append(values)

    def plot(self, labels: list = None):
        """
        Plot function for boxplot.
        :param labels: if not None, it defines the labels for x-axis of boxplot
        """
        data = self.counters_values

        bp = pyplot.boxplot(data, showmeans=True, patch_artist=True, labels=labels)
        for patch, color in zip(bp['boxes'], self.colors):
            patch.set_facecolor(color)


class HistType(Enum):
    LINE = 1
    BAR = 2


class Histogram(object):

    """
    Histogram can take values for statistics and plot a histogram from them.

    Values are added to the internal array. The class is able to generate a histogram and plot it using pyplot.


    """

    # colors for plotting multiple plots in one figure
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

    def __init__(self):
        """
        Constructor for a simple histogram
        """
        self.counters_values = []
        self.n_bins = 0
        self.weights = None

    def add_counter_data(self, values : list, weights: list=None):
        """
        Add a value to the histogram.
        :param values: the list of values of a counter to be plotted
        :param weights: the list of weights of a counter if this counter is TDC
        """
        #######################################
        # DONE Task 3.2.1:
        self.counters_values.append(values)
        if weights is not None:
            if self.weights is None:
                self.weights = []
            self.weights.append(weights)
        #######################################

    def reset(self):
        """
        Reset all values to their initial state.
        """
        self.counters_values = []
        self.n_bins = 0
        self.weights = None

    def plot(self, diag_type: HistType = HistType.BAR, labels: list=None, n_bins: int=None):
        """
        Plot function for histogram.
        :param diag_type: is the type of the histogram - Bar or Line
        :param labels: if not None, specifies labels for x-axis
        :param n_bins: if not None, specifies number of bins
        """
        #######################################
        # DONE Task 3.2.2:
        if n_bins is None:
            self.n_bins = int(np.sqrt(len(self.counters_values[0])))
        else:
            self.n_bins = n_bins
        if diag_type == HistType.LINE:
            """
            Plot line plot - mainly thought for mean waiting time
            """
            pyplot.hist(self.counters_values, weights=self.weights, bins=self.n_bins, histtype='step', linestyle="-", label=labels, density=True)

        elif diag_type == HistType.BAR:
            """
            Plot side-by-side histogram plot - mainly thought for mean queue length
            """
            pyplot.hist(self.counters_values, weights=self.weights, bins=self.n_bins, histtype='bar', label=labels, density=True)

        if labels is not None:
            pyplot.legend(loc='upper right')
        #######################################


class Heatmap(object):
    def __init__(self):
        """
        Constructor for a heatmap of correlations
        """
        self.corr_dict = {}

    def add_corr_coef(self, par1: str, par2: str, value: float):
        """
        Add correlation value and parameters to the internal dict.
        :param par1: string corresponding to the name of the first parameter in the correlation
        :param par2: string corresponding to the name of the second parameter in the correlation
        :param value: correlation value
        """
        #######################################
        # TODO Task 4.1.3: Your code goes here
        
        if par1 not in self.corr_dict:
            self.corr_dict[par1] = {}
        if par2 not in self.corr_dict:
            self.corr_dict[par2] = {}
        self.corr_dict[par1][par2] = value
        self.corr_dict[par2][par1] = value
        #######################################

    def plot(self):
        """
        Plot heatmap as a square table where the correlation of each two parameters is shown.
        If the corresponding value is absent, nan will be shown.
        """
        #######################################
        # TODO Task 4.1.3: Your code goes here
        keys = list(self.corr_dict.keys())
        size = len(keys)
        
        data = np.full((size, size), np.nan)
     
        for i, key1 in enumerate(keys):
            for j, key2 in enumerate(keys):
                if key2 in self.corr_dict[key1]:
                    data[i, j] = self.corr_dict[key1][key2]

        fig, ax = pyplot.subplots()
        cax = ax.imshow(data, cmap='inferno', vmin=-1, vmax=1)

 
        ax.set_xticks(np.arange(size))
        ax.set_yticks(np.arange(size))
        ax.set_xticklabels(keys)
        ax.set_yticklabels(keys)

    
        pyplot.setp(ax.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")

    
        for i in range(size):
            for j in range(size):
                text = ax.text(j, i, f'{data[i, j]:.2f}' if not np.isnan(data[i, j]) else '',
                               ha="center", va="center", color="w")

      
        fig.colorbar(cax, ax=ax)

        pyplot.show()
        #######################################
