import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
from counter import TimeIndependentCounter
# class TimeIndependentCounter:
#     def __init__(self, name="default"):
#         self.name = name
#         self.values = []

#     def count(self, value: float):
#         self.values.append(value)

#     def get_mean(self):
#         if len(self.values) > 0:
#             return np.mean(self.values)
#         else:
#             return None

#     def get_var(self, biased=False):
#         if biased:
#             return np.var(self.values)
#         else:
#             return np.var(self.values, ddof=1)

#     def get_stddev(self):
#         return np.sqrt(self.get_var())

#     def report_confidence_interval(self, alpha: float = 0.05):
#         if len(self.values) == 0:
#             return None

#         n = len(self.values)
#         mean = self.get_mean()
#         std_dev = self.get_stddev()

#         t_critical = scipy.stats.t.ppf(1 - alpha / 2, df=n-1)
#         half_width = t_critical * (std_dev / np.sqrt(n))

#         lower_bound = mean - half_width
#         upper_bound = mean + half_width

#         return lower_bound, upper_bound, half_width * 2

def simulate_queue(lambda_, mu, S, simulation_time):
    # Initialize variables
    arrival_time = np.random.exponential(1 / lambda_)
    departure_time = float('inf')
    num_in_system = 0
    total_blocked = 0
    total_arrivals = 0
    current_time = 0

    while current_time < simulation_time:
        if arrival_time <= departure_time and arrival_time <= simulation_time:
            # Process arrival
            current_time = arrival_time
            total_arrivals += 1
            if num_in_system < S:
                num_in_system += 1
                if num_in_system == 1:
                    departure_time = current_time + np.random.exponential(1 / mu)
            else:
                total_blocked += 1

            arrival_time = current_time + np.random.exponential(1 / lambda_)
        else:
            # Process departure
            current_time = departure_time
            num_in_system -= 1
            if num_in_system > 0:
                departure_time = current_time + np.random.exponential(1 / mu)
            else:
                departure_time = float('inf')

    blocking_probability = total_blocked / total_arrivals
    return blocking_probability

def task_5_2_1(lambda_, mu, S, simulation_time, epsilon, confidence_level):
    tic = TimeIndependentCounter("Blocking Probability")
    target_width = 2 * epsilon

    while True:
        blocking_probability = simulate_queue(lambda_, mu, S, simulation_time)
        tic.count(blocking_probability)

        _, _, ci_width = tic.report_confidence_interval(alpha=(1-confidence_level))

        if ci_width < target_width:
            break

    return tic.get_mean(), tic.report_confidence_interval(alpha=(1-confidence_level)), len(tic.values)

def task_5_2_2(lambda_, mu, S, batch_size, epsilon, confidence_level):
    tic = TimeIndependentCounter("Blocking Probability")
    target_width = 2 * epsilon
    total_arrivals = 0

    while True:
        blocking_probability = simulate_queue(lambda_, mu, S, batch_size)
        tic.count(blocking_probability)

        _, _, ci_width = tic.report_confidence_interval(alpha=(1-confidence_level))

        if ci_width < target_width:
            break

        total_arrivals += batch_size

    return tic.get_mean(), tic.report_confidence_interval(alpha=(1-confidence_level)), total_arrivals

def task_5_2_3(intervals, title):
    means = [mean for mean, _, _ in intervals]
    lower_bounds = [lb for _, (lb, _, _), _ in intervals]
    upper_bounds = [ub for _, (_, ub, _), _ in intervals]

    plt.figure(figsize=(10, 5))
    x = list(range(1, len(intervals) + 1))
    plt.errorbar(x, means, yerr=[np.array(means) - np.array(lower_bounds), np.array(upper_bounds) - np.array(means)], fmt='o', capsize=5)
    plt.title(title)
    plt.xlabel('Sample')
    plt.ylabel('Mean value with confidence interval')
    plt.show()

def task_5_2_4():
    lambda_1 = 1 / 1000
    mu_1 = 1 / 900
    mu_2 = 1 / 500
    epsilon = 0.0015

    results = []

    for traffic_intensity, mu in [(0.5, mu_1), (0.9, mu_2)]:
        for confidence_level in [0.9, 0.95]:
            for sim_time in [100, 1000]:
                intervals = []
                for _ in range(30):
                    mean, ci, _ = task_5_2_1(lambda_1, mu, 1, sim_time, epsilon, confidence_level)
                    intervals.append((mean, ci, sim_time))
                results.append((intervals, f"Traffic intensity {traffic_intensity}, Confidence level {confidence_level}, Simulation time {sim_time}"))

    for intervals, title in results:
        task_5_2_3(intervals, title)

if __name__ == "__main__":
    lambda_ = 1 / 1000
    mu = 1 / 900
    S = 4
    epsilon = 0.0015

    # Task 5.2.1: Multiple Runs Confidence
    mean_90, ci_90, runs_90 = task_5_2_1(lambda_, mu, S, 100, epsilon, 0.9)
    print(f"Task 5.2.1 - Confidence level 0.9: Mean={mean_90}, CI={ci_90}, Runs={runs_90}")

    mean_95, ci_95, runs_95 = task_5_2_1(lambda_, mu, S, 100, epsilon, 0.95)
    print(f"Task 5.2.1 - Confidence level 0.95: Mean={mean_95}, CI={ci_95}, Runs={runs_95}")

    # Repeat with simulation time 1000s
    mean_90_1000, ci_90_1000, runs_90_1000 = task_5_2_1(lambda_, mu, S, 1000, epsilon, 0.9)
    print(f"Task 5.2.1 - Confidence level 0.9 (1000s): Mean={mean_90_1000}, CI={ci_90_1000}, Runs={runs_90_1000}")

    mean_95_1000, ci_95_1000, runs_95_1000 = task_5_2_1(lambda_, mu, S, 1000, epsilon, 0.95)
    print(f"Task 5.2.1 - Confidence level 0.95 (1000s): Mean={mean_95_1000}, CI={ci_95_1000}, Runs={runs_95_1000}")

    # Task 5.2.2: Batch Confidence
    mean_90_batch, ci_90_batch, total_arrivals_90_batch = task_5_2_2(lambda_, mu, S, 100, epsilon, 0.9)
    print(f"Task 5.2.2 - Batch Confidence level 0.9: Mean={mean_90_batch}, CI={ci_90_batch}, Total Arrivals={total_arrivals_90_batch}")

    mean_95_batch, ci_95_batch, total_arrivals_95_batch = task_5_2_2(lambda_, mu, S, 100, epsilon, 0.95)
    print(f"Task 5.2.2 - Batch Confidence level 0.95: Mean={mean_95_batch}, CI={ci_95_batch}, Total Arrivals={total_arrivals_95_batch}")

    # Task 5.2.3: Confidence Plots I
    intervals_90 = [(mean_90, ci_90, runs_90), (mean_90_1000, ci_90_1000, runs_90_1000), (mean_90_batch, ci_90_batch, total_arrivals_90_batch)]
    task_5_2_3(intervals_90, "Confidence Intervals for Confidence Level 0.9")

    intervals_95 = [(mean_95, ci_95, runs_95), (mean_95_1000, ci_95_1000, runs_95_1000), (mean_95_batch, ci_95_batch, total_arrivals_95_batch)]
    task_5_2_3(intervals_95, "Confidence Intervals for Confidence Level 0.95")

    # Task 5.2.4: Confidence Plots II
    task_5_2_4()
