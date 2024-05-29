from matplotlib import pyplot
import random
from simparam import SimParam
from simulation import Simulation
from counter import TimeIndependentCounter
from plothelpers import BoxPlot
from matplotlib import pyplot
import numpy as np

"""
This file should be used to keep all necessary code that is used for the simulation study in part 2 of the programming
assignment. It contains the tasks 2.7.1 and 2.7.2.

The function do_simulation_study() should be used to run the simulation routine, that is described in the assignment.
"""


def task_2_7_1_2():
    """
    Here, we execute tasks 2.7.1 and 2.7.2 in the same function. This makes sense, since we use only one figure with
    four subfigures to display the plots, which makes comparability easier.
    """
    sim_param = SimParam()
    sim_param.NUM_RUNS = 1000
    sim = Simulation(sim_param)
    bp_wt_1, bp_ql_1 = do_simulation_study(sim, "SIM_TIME = 100s")

    sim_param.SIM_TIME = 1000000
    bp_wt_2, bp_ql_2 = do_simulation_study(sim, "SIM_TIME = 1000s")

    pyplot.rcParams['axes.grid'] = True

    pyplot.subplot(221)
    pyplot.ylabel("Mean waiting time [ms]")
    pyplot.ylim(500, 3000)
    bp_wt_1.plot(labels=["5", "6", "7"])
    pyplot.title("SIM_TIME = 100s")

    pyplot.subplot(223)
    pyplot.ylabel("Mean queue length")
    pyplot.xlabel("Buffer volume")
    pyplot.ylim(0, 7)
    bp_ql_1.plot(labels=["5", "6", "7"])

    pyplot.subplot(222)
    pyplot.ylim(500, 3000)
    pyplot.title("SIM_TIME = 1000s")
    bp_wt_2.plot(labels=["5", "6", "7"])

    pyplot.subplot(224)
    pyplot.ylim(0, 7)
    pyplot.xlabel("Buffer volume")
    bp_ql_2.plot(labels=["5", "6", "7"])

    pyplot.tight_layout()
    pyplot.show()


def task_2_7_3():
    """
    Here, we execute tasks 2.7.3.
    """
    sim_param = SimParam()
    sim_param.NUM_RUNS = 1000
    sim_param.NUM_SERVERS = 2
    sim_param.SERVICE_RATES = [0.00075, 0.00075]
    sim = Simulation(sim_param)
    bp_wt_1, bp_ql_1 = do_simulation_study(sim, "SIM_TIME = 100s")

    sim_param.SIM_TIME = 1000000
    sim.reset()
    bp_wt_2, bp_ql_2 = do_simulation_study(sim, "SIM_TIME = 1000s")

    pyplot.rcParams['axes.grid'] = True

    pyplot.subplot(221)
    pyplot.ylabel("Mean waiting time [ms]")
    pyplot.ylim(500, 3000)
    bp_wt_1.plot(labels=["5", "6", "7"])
    pyplot.title("SIM_TIME = 100s")

    pyplot.subplot(223)
    pyplot.ylabel("Mean queue length")
    pyplot.xlabel("Buffer volume")
    pyplot.ylim(0, 7)
    bp_ql_1.plot(labels=["5", "6", "7"])

    pyplot.subplot(222)
    pyplot.ylim(500, 3000)
    pyplot.title("SIM_TIME = 1000s")
    bp_wt_2.plot(labels=["5", "6", "7"])

    pyplot.subplot(224)
    pyplot.ylim(0, 7)
    pyplot.xlabel("Buffer volume")
    bp_ql_2.plot(labels=["5", "6", "7"])

    pyplot.tight_layout()
    pyplot.show()


def do_simulation_study(sim, study_name: str):
    """
    This simulation study is different from the one made in assignment 1. It is mainly used to gather and visualize
    statistics for different buffer sizes S instead of finding a minimal number of spaces for a desired quality.
    For every buffer size S (which ranges from 5 to 7), statistics are printed (depending on the input parameters).
    Finally, after all runs, the results are plotted in order to visualize the differences and giving the ability
    to compare them. The simulations are run first for 100s, then for 1000s. For each simulation time, two diagrams are
    shown: one boxplot of the mean waiting times and one of the average buffer usage
    :param sim: the simulation object to do the simulation
    """
    random.seed(0)
    bp_wt = BoxPlot()
    bp_ql = BoxPlot()

    counter_mean_waiting_time = TimeIndependentCounter("Mean waiting time, " + study_name)
    counter_mean_queue_length = TimeIndependentCounter("Mean queue length, " + study_name)

    # step through number of buffer spaces...
    s_val = [5, 6, 7]
    for S in s_val:
        print("S = ", S)
        sim.sim_param.S = S

        counter_mean_waiting_time.reset()
        counter_mean_queue_length.reset()

        # repeat simulation
        for run in range(sim.sim_param.NUM_RUNS):
            sim.reset()
            sim.do_simulation()
            counter_mean_waiting_time.count(sim.statistics_collection.cnt_wt.get_mean())
            counter_mean_queue_length.count(sim.statistics_collection.cnt_ql.get_mean())
        counter_mean_waiting_time.report()
        counter_mean_queue_length.report()
        bp_wt.add_counter_data(counter_mean_waiting_time.values)
        bp_ql.add_counter_data(counter_mean_queue_length.values)

    return bp_wt, bp_ql


def study_waiting_time():
    random.seed(0)
    sim_param = SimParam()
    sim_param.NUM_RUNS = 100
    sim_param.S = 5
    sim = Simulation(sim_param)
    waiting_times = np.empty((sim_param.NUM_RUNS, 120))
    for run in range(sim.sim_param.NUM_RUNS):
        sim.reset()
        sim.do_simulation()
        waiting_times[run] = np.array(sim.statistics_collection.cnt_wt.values[:120])

    sim_param.SIM_TIME = 1000000
    waiting_times_1 = np.empty((sim_param.NUM_RUNS, 1200))
    for run in range(sim.sim_param.NUM_RUNS):
        sim.reset()
        sim.do_simulation()
        waiting_times_1[run] = np.array(sim.statistics_collection.cnt_wt.values[:1200])

    pyplot.rcParams['axes.grid'] = True

    pyplot.subplot(211)
    pyplot.xlabel('Packet number')
    pyplot.ylabel('Waiting time [ms]')
    pyplot.title('100s')
    pyplot.plot(np.mean(waiting_times, axis=0))

    pyplot.subplot(212)
    pyplot.xlabel('Packet number')
    pyplot.ylabel('Waiting time [ms]')
    pyplot.title('1000s')
    pyplot.plot(np.mean(waiting_times_1, axis=0))
    pyplot.tight_layout()
    pyplot.show()


if __name__ == '__main__':
    task_2_7_1_2()
    task_2_7_3()
    study_waiting_time()
