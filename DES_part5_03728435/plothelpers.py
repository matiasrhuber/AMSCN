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
        # DONE Task 4.1.3:
        if par1 not in self.corr_dict.keys():
            self.corr_dict[par1] = {}
        if par2 not in self.corr_dict.keys():
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
        # DONE Task 4.1.3:
        par_list = list(self.corr_dict.keys())
        corr_list = np.empty((len(par_list), len(par_list)))

        # fill the 2d array with correlations
        for i in range(len(par_list)):
            for j in range(len(par_list)):
                if par_list[i] in self.corr_dict.keys():
                    if par_list[j] in self.corr_dict[par_list[i]].keys():
                        corr_list[i][j] = self.corr_dict[par_list[i]][par_list[j]]
                        corr_list[j][i] = self.corr_dict[par_list[i]][par_list[j]]
                        continue
                corr_list[j][i] = None

        # plotting heatmap
        heatmap = pyplot.imshow(corr_list, cmap='inferno', vmin=-1, vmax=1)
        pyplot.xticks(np.arange(len(par_list)), par_list, rotation=90)
        pyplot.yticks(np.arange(len(par_list)), par_list)

        # plotting colorbar as a legend
        pyplot.colorbar(heatmap)

        # inserting correlation values to the heatmap
        for i in range(len(par_list)):
            for j in range(len(par_list)):
                pyplot.text(j, i, np.round(corr_list[i, j], 1), ha="center", va="center", color="k")
        #######################################
