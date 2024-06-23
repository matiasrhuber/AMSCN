# simstudy5.py

import numpy as np
from scipy.stats import norm
from simulation import Simulation
from simparam import SimParam
from statisticscollection import StatCollection
from counter import TimeIndependentCounter
import matplotlib.pyplot as plt
from scipy.stats import t

def task_5_2_1(epsilon, confidence_level=0.95, sim_time=1000):

    tic = TimeIndependentCounter("Blocking Probability")
    sim_param = SimParam()
    sim_param.SIM_TIME = sim_time
    sim_param.lambda_ = 1 / 1000
    sim_param.mu = 1 / 900
    sim_param.S = 4
    
    while True:
        sim = Simulation(sim_param)
        result = sim.do_simulation()
        blocking_probability = result.blocking_probability  # Assuming such a method exists
        tic.count(blocking_probability)
        
        if len(tic.values) > 1:
            ci_width = tic.report_confidence_interval(alpha=1 - confidence_level, print_report=False)
            if ci_width < 2 * epsilon:
                break
    
    return tic.values, ci_width

def task_5_2_2(epsilon, confidence_level=0.95, N=100):

    blocking_probabilities = []
    sim_param = SimParam()
    sim_param.lambda_ = 1 / 1000
    sim_param.mu = 1 / 900
    sim_param.S = 4

    tic = TimeIndependentCounter("blocking_probability")
    sim = Simulation(sim_param)

    while True:
        result = sim.do_simulation_n_limit(N)
        blocking_probability = result.blocking_probability
        tic.count(blocking_probability)
        blocking_probabilities.append(blocking_probability) #alternatice to tic

        sim.reset()

        if len(tic.values) > 1:
            ci_width = tic.report_confidence_interval(alpha=1 - confidence_level, print_report=False)
            if ci_width < 2 * epsilon:
                break

    total_sim_time = sim.sys_state.now
    return blocking_probabilities, ci_width, total_sim_time

def task_5_2_3(blocking_probabilities, confidence_intervals):
    print(blocking_probabilities)
    #if np.ndim(blocking_probabilities) == 1:
        # If blocking_probabilities is 1-dimensional, convert it to a 2-dimensional array with one row
    #    blocking_probabilities = np.array([blocking_probabilities])
    
    num_samples = len(blocking_probabilities)
    print(num_samples, "NUM OF SAMPLES")
    sample_ids = np.arange(1, num_samples + 1)
    print(sample_ids, "IDS")
    #blocking_probabilities = np.array([blocking_probabilities])

    # Calculate mean value and lower/upper bounds of confidence intervals
    means = np.mean(blocking_probabilities)
    lower_bounds = means - confidence_intervals[:, 0]
    upper_bounds = confidence_intervals[:, 1] - means

    # Plotting
    print(means)
    plt.errorbar(sample_ids, blocking_probabilities, fmt='o', capsize=5)
    plt.xlabel('Sample ID (Confidence Interval)')
    plt.ylabel('Blocking Probability')
    plt.title('Mean Blocking Probability with Confidence Intervals')
    plt.grid(True)
    plt.xticks(sample_ids)
    plt.show()



def task_5_2_4():
    # Define simulation parameters
    num_runs = 30  # Number of runs per simulation
    num_repetitions = 100  # Number of repetitions
    sim_times = [100, 1000]
    traffic_params = [
        (1 / 1000, 1 / 900),
        (1 / 1000, 1 / 500)
    ]
    confidence_levels = [0.9, 0.95]

    # Initialize arrays to store results
    results = np.zeros((len(sim_times), len(traffic_params), len(confidence_levels), num_repetitions, num_runs))

    for t_idx, sim_time in enumerate(sim_times):
        for tp_idx, traffic_param in enumerate(traffic_params):
            for cl_idx, confidence_level in enumerate(confidence_levels):
                # Initialize SimParam with appropriate parameters
                sim_params = SimParam()
                sim_params.SIM_TIME = sim_time
                sim_params.NUM_SERVERS = 1
                sim_params.SERVICE_RATES = [traffic_param[1]]  # Ensure SERVICE_RATES is a list
                sim_params.SERVERS_SEEDS = [12345]  # Example seeds, ensure it's a list

                # Perform simulations and collect results
                for rep in range(num_repetitions):
                    simulation = Simulation(sim_param=sim_params)
                    statistics = simulation.do_simulation_n_limit(num_runs)
                    utilization_values = statistics.blocking_probability

                    # Calculate confidence intervals
                    mean_utilization = np.mean(utilization_values)
                    std_dev_utilization = np.std(utilization_values)
                    ci_half_width = std_dev_utilization * 1.96 / np.sqrt(num_runs)  # 95% confidence interval
                    
                    # Store results
                    results[t_idx, tp_idx, cl_idx, rep, :] = [mean_utilization, ci_half_width]

    # Plotting code
    for t_idx, sim_time in enumerate(sim_times):
        for tp_idx, traffic_param in enumerate(traffic_params):
            for cl_idx, confidence_level in enumerate(confidence_levels):
                plt.figure()
                for rep in range(num_repetitions):
                    # Extract mean and confidence interval for this repetition
                    mean_value = results[t_idx, tp_idx, cl_idx, rep, 0]
                    ci_value = results[t_idx, tp_idx, cl_idx, rep, 1]

                    # Plotting with error bars
                    plt.errorbar(rep + 1, mean_value, yerr=ci_value, fmt='o', capsize=5)

                # Add theoretical value as dashed line (if applicable)
                # plt.axhline(theoretical_value, color='r', linestyle='--')

                # Plot labels and title
                plt.xlabel('Repetitions')
                plt.ylabel('Mean Utilization')
                plt.title(f'Simulation Results (Sim Time: {sim_time}, Traffic Params: {traffic_param}, Confidence Level: {confidence_level})')
                plt.grid(True)
                plt.tight_layout()

                # Save or show plot
                plt.savefig(f'simulation_results_{sim_time}_{traffic_param}_{confidence_level}.png')
                plt.show()
# Example usage
if __name__ == "__main__":
    epsilon = 0.01
    confidence_level = 0.95
    #blocking_probabilities, ci_width = task_5_2_1(epsilon, confidence_level)
    #print(f"Blocking probabilities: {blocking_probabilities}")
    #print(f"Final confidence interval width: {ci_width}")

    N = 100
    blocking_probabilities, ci_width, total_sim_time = task_5_2_2(epsilon, confidence_level, N)
    print(f"Blocking probabilities: {blocking_probabilities}")
    print(f"Final confidence interval width: {ci_width}")
    print(f"Total simulation time: {total_sim_time}")#

    confidence_intervals = np.array([[mean - ci_width / 2, mean + ci_width / 2] for mean in blocking_probabilities])
    task_5_2_3(blocking_probabilities, confidence_intervals)
    #task_5_2_4()
