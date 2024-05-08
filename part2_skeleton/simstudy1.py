import matplotlib.pyplot as plt

from simparam import SimParam
from simulation import Simulation
import random

import numpy as np

"""
This file should be used to keep all necessary code that is used for the simulation study in part 1 of the programming
assignment. It contains the tasks 1.7.1, 1.7.2 and the bonus task 1.7.3.

The function do_simulation_study() should be used to run the simulation routine, that is described in the assignment.
"""


def task_1_7_1():
    """
    Execute task 1.7.1 and perform a simulation study according to the task assignment.
    :return: Minimum number of buffer spaces to meet requirements.
    """
    random.seed(5722157)
    sim = Simulation()
    return do_simulation_study(sim, 5)


def task_1_7_2():
    """
    Execute task 1.7.2 and perform a simulation study according to the task assignment.
    :return: Minimum number of buffer spaces to meet requirements.
    """
    sim_param = SimParam()
    random.seed(5722157)
    sim_param.SERVICE_RATE = 0.015
    sim = Simulation(sim_param)
    return do_simulation_study(sim, 50)


def task_1_7_3():
    """
    Execute bonus task 1.7.3.
    """
    rho = 0.95
    service_rate_list = [0.002, 0.005, 0.01]
    sim = Simulation()
    for service_rate in service_rate_list:
        sim.sim_param.SERVICE_RATE = service_rate
        sim.sim_param.ARRIVAL_RATE = rho_to_lambda(rho, sim.sim_param)
        drop_rate_list = []
        for __ in range(sim.sim_param.NUM_RUNS):
            sim.reset()
            sim.do_simulation()
            drop_rate_list.append(sim.sys_state.get_blocking_probability())
        plt.plot(np.sort(drop_rate_list), np.array(range(sim.sim_param.NUM_RUNS))/ sim.sim_param.NUM_RUNS,
                 label="$\mu = $" + str(service_rate))
    plt.grid()
    plt.xlabel("Blocking probability")
    plt.ylabel("CDF")
    plt.legend()
    plt.show()





def lambda_to_rho(lam: float, sim_param: SimParam):
    mu = sim_param.SERVICE_RATE
    return lam/mu


def rho_to_lambda(rho: float, sim_param: SimParam):
    mu = sim_param.SERVICE_RATE
    return rho * mu


def do_simulation_study(sim, max_dropped):
    """
    This function performs the simulation study. Study runs as follows:
    simulation goal: in 80% of all runs only 10 packets dropped (see simparam.MAX_DROPPED for this value)
    If simulation goal is missed by far (< 70% or > 90%), the number of buffer spaces is raised by one
    If simulation goal is met or almost met: more runs are made with same number of buffer spaces
    to see whether it's just happened by an unfortunate choosing of random numbers (establish confidence).
    """
    go_on = True
    sign = 1
    max_dropped = max_dropped

    additional_runs = 3
    fails_add_runs = 0

    rho = 1.0

    sim.sim_param.ARRIVAL_RATE = rho_to_lambda(rho, sim.sim_param)

    while go_on:
        num_successful_runs = 0
        for __ in range(sim.sim_param.NUM_RUNS):
            sim.reset()
            sim.do_simulation()
            if sim.sys_state.packets_dropped < max_dropped:
                num_successful_runs += 1

        print("RHO: " + str(round(sim.sim_param.ARRIVAL_RATE/sim.sim_param.SERVICE_RATE, 2)) + " GOOD/TOTAL: " +
              str(num_successful_runs) + "/" + str(sim.sim_param.NUM_RUNS) + " PERCENT: " + str(
            100 * num_successful_runs / sim.sim_param.NUM_RUNS) + "%")

        # close to criterion: make more runs to ensure, that the result is not only forced
        # by a fortunate or unfortunate choosing of random numbers
        if float(num_successful_runs) / float(sim.sim_param.NUM_RUNS) >= .9 and go_on:
            # we may need to stop the simulation
            go_on = False
            fails_add_runs = 0
            for run in range(additional_runs):
                # sim.sim_param.R - 1 defines, how many more runs are made if close to criterion
                num_successful_runs = 0

                for _ in range(sim.sim_param.NUM_RUNS):
                    sim.reset()
                    sim.do_simulation()
                    if sim.sys_state.packets_dropped < max_dropped:
                        num_successful_runs += 1

                print("RHO: " +  str(round(sim.sim_param.ARRIVAL_RATE/sim.sim_param.SERVICE_RATE, 2)) + " GOOD/TOTAL: " +
                      str(num_successful_runs) + "/" + str(sim.sim_param.NUM_RUNS) + " PERCENT: " + str(
                    100 * num_successful_runs / sim.sim_param.NUM_RUNS) + "%")

                # we need at least two out of three simulations to output more than 0.8 values in order to be confident
                if float(num_successful_runs) / float(sim.sim_param.NUM_RUNS) < .95:
                    fails_add_runs += 1
            if fails_add_runs >= 2:
                go_on = True
        if go_on and sign == 1:
            # make rho smaller if criterion is not fulfilled sufficiently yet
            rho -= 0.1
            sim.sim_param.ARRIVAL_RATE = rho_to_lambda(rho, sim.sim_param)

        elif go_on and sign == 2:
            rho -= 0.01
            sim.sim_param.ARRIVAL_RATE = rho_to_lambda(rho, sim.sim_param)

        elif not go_on and sign == 1:
            go_on = True
            rho += 0.09
            sign = 2
            sim.sim_param.ARRIVAL_RATE = rho_to_lambda(rho, sim.sim_param)

    return round(sim.sim_param.ARRIVAL_RATE / sim.sim_param.SERVICE_RATE, 2)


if __name__ == '__main__':
    #task_1_7_1()
    #task_1_7_2()
    task_1_7_3()