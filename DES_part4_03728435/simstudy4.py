import numpy as np
from counter import TimeIndependentAutocorrelationCounter, TimeIndependentCrosscorrelationCounter
from plothelpers import Heatmap
from simulation import Simulation
from simparam import SimParam
from statisticscollection import StatCollection
from matplotlib import pyplot as plt

def task_4_2_1():
 
    sequence_1 = [5, -5, 5, -5, 5, -5, 5, -5]
    sequence_2 = [3, -5, 5, -1, 3, -5, 5, -1, 3]

    max_lag = 4 # lowest common multiple of 2 and 4

    auto_corr_counter_1 = TimeIndependentAutocorrelationCounter(max_lag=max_lag)
    auto_corr_counter_2 = TimeIndependentAutocorrelationCounter(max_lag=max_lag)

    # for value1, value2 in zip(sequence_1, sequence_2):
    #     auto_corr_counter_1.count(value1,value2)
    for x in sequence_1:
        auto_corr_counter_1.count(x)

    for x in sequence_2:
        auto_corr_counter_2.count(x)

    print('sequence 1', sequence_1)

    auto_corr_counter_1.report()

    print('sequence 2', sequence_2)
    auto_corr_counter_2.report()

def run_simulation(traffic_rate, service_rate, num_users, queue_size, simulation_time):

    sim_param = SimParam(
        S=queue_size,
        SIM_TIME=simulation_time,
        NUM_USERS=num_users,
        ARRIVAL_RATES=[traffic_rate]* num_users,
        NUM_SERVERS=1,
        SERVICE_RATES=[service_rate],
        USERS_SEEDS= range(0,num_users)
    )
    simulation = Simulation(sim_param=sim_param)
    simulation.do_simulation() #possibly not necessary
    stats_collected = StatCollection(sim=simulation)
    return simulation.statistics_collection #stats_collected # #stats_collected.gather_results() 

def visualize_correlations(stat_collections, traffic_rates):

    heatmap = Heatmap()

    for stat in stat_collections:
        print('traffic rates:',traffic_rates)
        print('IAT WT Correlation:',stat.cnt_iat_wt.get_cor())
        print('IAT ST Correlation:',stat.cnt_iat_st.get_cor())
        print('IAT SYST Correlation:',stat.cnt_iat_syst.get_cor())
        print('ST SYST Correlation:',stat.cnt_st_syst.get_cor())
        print('WT1 WT2 Correlation:',stat.cnt_wt1_wt2.get_cor())
        heatmap.add_corr_coef('IAT', 'Waiting Time', stat.cnt_iat_wt.get_cor())
        heatmap.add_corr_coef('IAT', 'Service Time', stat.cnt_iat_st.get_cor())
        heatmap.add_corr_coef('IAT', 'System Time', stat.cnt_iat_syst.get_cor())
        heatmap.add_corr_coef('Service Time', 'System Time', stat.cnt_st_syst.get_cor())
        heatmap.add_corr_coef('Waiting Time User 1', 'Waiting Time User 2', stat.cnt_wt1_wt2.get_cor())

    # raise ValueError
    heatmap.plot()

def visualize_autocorrelation_wt(stat_collections, traffic_rates):

    heatmap = Heatmap()
 
    for stat in stat_collections:
        # for lag1 in range(1, 21):
        #     for lag2 in range(1, 21):
        for lag in range(1,21):
            heatmap.add_corr_coef(f'Autocorrelation (Waiting Time lag={lag})', f'Autocorrelation (Waiting Time lag={lag})', stat.acnt_wt.get_auto_cor(lag))
    heatmap.plot()

def visualize_autocorrelation_iat(stat_collections, traffic_rates):

    heatmap = Heatmap()
 
    for stat in stat_collections:
        # for lag1 in range(1, 21):
        #     for lag2 in range(1, 21):
        for lag in range(1, 11):
            heatmap.add_corr_coef(f'Autocorrelation (Inter-arrival Time lag={lag})', f'Autocorrelation (Inter-arrival Time lag={lag})', stat.acnt_iat.get_auto_cor(lag))
    heatmap.plot()



def task_4_3_1():
    A = [0.01, 0.5, 0.8, 0.95]
    mu = 0.015 #[0.015]*len(A)
    simulation_time = 10000
    queue_size = 10000
    num_users = 2
    stat_collections = []

    # print(f"Running simulation for traffic rate: {A}")
    # stat_collections.append(run_simulation(A, mu, num_users, queue_size, simulation_time))

    for traffic_rate in A:
        print(f"Running simulation for traffic rate: {traffic_rate}")
        stat_collections.append(run_simulation(traffic_rate, mu, num_users, queue_size, simulation_time))
        visualize_correlations(stat_collections, traffic_rate)
        visualize_autocorrelation_wt(stat_collections, traffic_rate)
        visualize_autocorrelation_iat(stat_collections, traffic_rate)


def visualize_relationships_iat_st(stat_collections, traffic_rates):

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    print(axes)

    axes[0,0].scatter(stat_collections[0].cnt_iat_st.x_values,stat_collections[0].cnt_iat_st.y_values)
    axes[0,0].set_title(f'TR: {traffic_rates[0]}')

    axes[0,1].scatter(stat_collections[1].cnt_iat_st.x_values,stat_collections[1].cnt_iat_st.y_values)
    axes[0,1].set_title(f'TR: {traffic_rates[1]}')

    axes[1,0].scatter(stat_collections[2].cnt_iat_st.x_values,stat_collections[2].cnt_iat_st.y_values)
    axes[1,0].set_title(f'TR: {traffic_rates[2]}')

    axes[1,1].scatter(stat_collections[3].cnt_iat_st.x_values,stat_collections[3].cnt_iat_st.y_values)
    axes[1,1].set_title(f'TR: {traffic_rates[3]}')

    plt.tight_layout()
    plt.show()

def visualize_relationships_st_syst(stat_collections, traffic_rates):

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    axes[0,0].scatter(stat_collections[0].cnt_st_syst.x_values,stat_collections[0].cnt_st_syst.y_values)
    axes[0,0].set_title(f'TR: {traffic_rates[0]}')
    print('traffic_rate:',traffic_rates[0])
    print('x_values:',stat_collections[0].cnt_st_syst.x_values)
    print('y_values:', stat_collections[0].cnt_st_syst.y_values)

    axes[0,1].scatter(stat_collections[1].cnt_st_syst.x_values,stat_collections[1].cnt_st_syst.y_values)
    axes[0,1].set_title(f'TR: {traffic_rates[1]}')
    print('traffic_rate:',traffic_rates[1])
    print('x_values:',stat_collections[1].cnt_st_syst.x_values)
    print('y_values:', stat_collections[1].cnt_st_syst.y_values)

    axes[1,0].scatter(stat_collections[2].cnt_st_syst.x_values,stat_collections[2].cnt_st_syst.y_values)
    axes[1,0].set_title(f'TR: {traffic_rates[2]}')
    print('traffic_rate:',traffic_rates[2])
    print('x_values:',stat_collections[2].cnt_st_syst.x_values)
    print('y_values:', stat_collections[2].cnt_st_syst.y_values)

    axes[1,1].scatter(stat_collections[3].cnt_st_syst.x_values,stat_collections[3].cnt_st_syst.y_values)
    axes[1,1].set_title(f'TR: {traffic_rates[3]}')
    print('traffic_rate:',traffic_rates[3])
    print('x_values:',stat_collections[3].cnt_st_syst.x_values)
    print('y_values:', stat_collections[3].cnt_st_syst.y_values)
    
    plt.tight_layout()
    plt.show()

def task_4_3_2():
    A = [0.01, 0.5, 0.8, 0.95]
    mu = 0.015
    simulation_time = 10000
    queue_size = 10000
    num_users = 2
    stat_collections = []

    for traffic_rate in A:
        print(f"Running simulation for traffic rate: {traffic_rate}")
        stat_collections.append(run_simulation(traffic_rate, mu, num_users, queue_size, simulation_time))
    print(stat_collections[0].cnt_iat_st.x_values)
    visualize_relationships_iat_st(stat_collections, A)
    visualize_relationships_st_syst(stat_collections, A)

def task_4_3_3():
    traffic_rates = [0.01, 0.5, 0.8, 0.95]
    N_values = [100, 10000]

    for N in N_values:
        for traffic_rate in traffic_rates:
            sim_param = SimParam(
                SIM_TIME=10000,  
                ARRIVAL_RATES=[traffic_rate],  # Offered traffic rate
                S=100000,  # Unlimited queue size
                NUM_USERS=1,  # Single server
                NUM_SERVERS=1,
                SERVICE_RATES=[0.015],  # Service rate
            )

            simulation = Simulation(sim_param)
            statistics_collection = simulation.do_simulation_n_limit(N)

            autocorrelation_values = [statistics_collection.acnt_wt.get_auto_cor(lag) for lag in range(1, 21)]

            plt.plot(range(1, 21), autocorrelation_values, label=f"A={traffic_rate}")

        plt.title(f"Autocorrelation of Waiting Time (N={N})")
        plt.xlabel("Lag")
        plt.ylabel("Autocorrelation")
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == '__main__':
    #task_4_2_1()
    #task_4_3_1()
    #task_4_3_2()
    task_4_3_3()