from matplotlib import pyplot
import random
from simparam import SimParam, ARR_PROCESS
from simulation import Simulation
from counter import TimeIndependentCounter
from plothelpers import BoxPlot, Histogram, HistType
from matplotlib import pyplot
import numpy as np
import scipy.stats

from statisticstest import ChiSquare, TestDist

"""
This file should be used to keep all necessary code that is used for the simulation study in part 3 of the programming
assignment. It contains the tasks 3.5.1 and 3.5.2.
"""


def task_3_5_1():
    num_users = [1, 2, 5, 10, 20, 50]
    for n in num_users:
        task_3_5_1_study(n)


def task_3_5_1_study(num_users):
    sim_param = SimParam()
    sim_param.SIM_TIME = 10000000
    sim_param.USERS_ARRIVAL_PROCESS = ARR_PROCESS.UNIFORM
    sim_param.NUM_USERS = num_users
    sim_param.ARRIVAL_RATES = [0.0015/sim_param.NUM_USERS for _ in range(sim_param.NUM_USERS)]
    sim_param.USERS_SEEDS = [i for i in range(sim_param.NUM_USERS)]
    sim = Simulation(sim_param)
    sim.reset()
    sim.do_simulation()

    hist = Histogram()
    hist.add_counter_data(sim.statistics_collection.cnt_iat.values)
    hist.plot(diag_type=HistType.BAR)
    x = np.arange(min(sim.statistics_collection.cnt_iat.values), max(sim.statistics_collection.cnt_iat.values), 1)
    pyplot.plot(x, scipy.stats.expon.pdf(x, scale=sim.statistics_collection.cnt_iat.get_mean()), label='tested distribution pdf')
    pyplot.legend()
    pyplot.grid()
    pyplot.xlabel('Inter-arrival time to the system [ms]')
    pyplot.ylabel('PDF')
    pyplot.title('NUM_USERS = ' + str(num_users))
    pyplot.show()

    emp_n, emp_x = np.histogram(sim.statistics_collection.cnt_iat.values, bins=int(np.sqrt(len(sim.statistics_collection.cnt_iat.values))), range=(0,max(sim.statistics_collection.cnt_iat.values)))
    chi_test = ChiSquare(emp_x, emp_n, distr=TestDist.EXPONENTIAL)
    chi_test.test_distribution(0.05, sim.statistics_collection.cnt_iat.get_mean(), est_parameters=1)
    chi_test.test_distribution(0.15, sim.statistics_collection.cnt_iat.get_mean(), est_parameters=1)


def task_3_5_2():
    cnt_bs = TimeIndependentCounter()
    cnt_iat = TimeIndependentCounter()


    sim_param = SimParam()
    sim_param.NUM_RUNS = 100
    sim_param.SIM_TIME = 100000
    sim_param.USERS_ARRIVAL_PROCESS = ARR_PROCESS.EXPONENTIAL
    sim = Simulation(sim_param)
    for num_servers in [1, 2, 3]:
        bp_bs = BoxPlot()
        bp_ar = BoxPlot()
        sim.sim_param.NUM_SERVERS = num_servers
        sim.sim_param.SERVERS_SEEDS = [i for i in range(num_servers)]
        sim.sim_param.SERVICE_RATES = [0.0015 for _ in range(num_servers)]
        for num_users in [2, 4, 6]:
            sim.sim_param.NUM_USERS = num_users
            sim.sim_param.ARRIVAL_RATES = [0.001 for _ in range(num_users)]
            sim.sim_param.USERS_SEEDS = [i for i in range(num_users)]
            cnt_bs.reset()
            cnt_iat.reset()
            for _ in range(sim.sim_param.NUM_RUNS):
                sim.reset()
                sim.do_simulation()
                cnt_iat.count(1 / sim.statistics_collection.cnt_iat.get_mean())
                cnt_bs.count(sim.statistics_collection.cnt_bs.get_mean())
            bp_bs.add_counter_data(cnt_bs.values)
            bp_ar.add_counter_data(cnt_iat.values)
        bp_ar.plot(labels=["2", "4", "6"])
        pyplot.grid()
        pyplot.xlabel('Number of users')
        pyplot.ylabel('Sum arrival rate [pkt/ms]')
        pyplot.title('NUM_SERVERS = ' + str(num_servers))
        pyplot.show()
        bp_bs.plot(labels=["2", "4", "6"])
        pyplot.grid()
        pyplot.xlabel('Number of users')
        pyplot.ylabel('Average number of busy servers')
        pyplot.title('NUM_SERVERS = ' + str(num_servers))
        pyplot.show()


if __name__ == '__main__':
    task_3_5_1()
    task_3_5_2()