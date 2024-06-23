from plothelpers import Heatmap
import matplotlib.pyplot as plt
from counter import TimeIndependentAutocorrelationCounter
from simulation import Simulation
from simparam import SimParam, ARR_PROCESS


def task_4_2_1():
    """
    Execute exercise 4.2.1, which is basically just a test for the auto correlation.
    """
    autocorrelation_test_counter = TimeIndependentAutocorrelationCounter("test sequence", max_lag=1)

    print('First test series:')

    # Test first series:
    for _ in range(5000):
        autocorrelation_test_counter.count(5)
        autocorrelation_test_counter.count(-5)

    print('Mean = ' + str(autocorrelation_test_counter.get_mean()))
    print('Var = ' + str(autocorrelation_test_counter.get_var()))
    autocorrelation_test_counter.report()

    print('____________________________________________')
    print('Second test series:')
    autocorrelation_test_counter.reset()
    autocorrelation_test_counter.set_max_lag(3)

    # Test second series
    for _ in range(5000):
        autocorrelation_test_counter.count(3)
        autocorrelation_test_counter.count(-5)
        autocorrelation_test_counter.count(5)
        autocorrelation_test_counter.count(-1)

    # print results
    print('Mean = ' + str(autocorrelation_test_counter.get_mean()))
    print('Var = ' + str(autocorrelation_test_counter.get_var()))

    autocorrelation_test_counter.report()


def task_4_3_1():
    """
    Run the correlation tests for given rho for all correlation counters in counter collection.
    After each simulation, print report results.
    SIM_TIME is set higher in order to avoid a large influence of startup effects
    """
    plt.rcParams["figure.figsize"] = (10, 10)
    sim_param = SimParam()
    sim_param.SIM_TIME = 10000000
    sim_param.NUM_USERS = 2
    sim_param.NUM_SERVERS = 1
    sim_param.SERVERS_SEEDS = [100]
    sim_param.USERS_SEEDS = [i for i in range(sim_param.NUM_USERS)]
    sim_param.SERVICE_RATES = [0.015]
    sim_param.S = 10000
    sim_param.ARRIVAL_RATES = [0.015 for _ in range(sim_param.NUM_USERS)]
    sim_param.USERS_ARRIVAL_PROCESS = ARR_PROCESS.EXPONENTIAL

    sim = Simulation(sim_param)

    for lam in [0.015/200, 0.015/4, 0.015*0.8/2, 0.015*0.95/2]:
        sim_param.ARRIVAL_RATES = [lam for _ in range(sim_param.NUM_USERS)]
        sim.reset()
        print('_____________________________________________________')
        print('NEW RUN with rho=' + str(lam/0.015*2))
        print('_____________________________________________________\n')
        sim.do_simulation()
        sim.statistics_collection.report()
        hm1 = Heatmap()
        for i in range(sim.statistics_collection.acnt_wt.max_lag + 1):
            for j in range(sim.statistics_collection.acnt_wt.max_lag + 1):
                hm1.add_corr_coef('wt, lag '+str(i), 'wt, lag '+str(j),
                                  sim.statistics_collection.acnt_wt.get_auto_cor((i-j)%(sim.statistics_collection.acnt_wt.max_lag+1)))
        plt.title('RHO = ' + str(lam/0.015*2))
        hm1.plot()
        plt.show()

        hm2 = Heatmap()
        hm2.add_corr_coef('iat', 'wt', sim.statistics_collection.cnt_iat_wt.get_cor())
        hm2.add_corr_coef('iat', 'st', sim.statistics_collection.cnt_iat_st.get_cor())
        hm2.add_corr_coef('iat', 'syst', sim.statistics_collection.cnt_iat_syst.get_cor())
        hm2.add_corr_coef('st', 'syst', sim.statistics_collection.cnt_st_syst.get_cor())
        hm2.add_corr_coef('wt1', 'wt2', sim.statistics_collection.cnt_wt1_wt2.get_cor())
        plt.title('RHO = ' + str(lam / 0.015 * 2))
        hm2.plot()
        plt.show()

        hm3 = Heatmap()
        for i in range(sim.statistics_collection.acnt_iat.max_lag + 1):
            for j in range(sim.statistics_collection.acnt_iat.max_lag + 1):
                hm3.add_corr_coef('iat, lag ' + str(i), 'iat, lag ' + str(j),
                                  sim.statistics_collection.acnt_iat.get_auto_cor(
                                      (i - j) % (sim.statistics_collection.acnt_iat.max_lag + 1)))
        plt.title('RHO = ' + str(lam / 0.015 * 2))
        hm3.plot()
        plt.show()


def task_4_3_2():
    """
    Exercise to plot the scatter plot of (a) IAT and serving time, (b) serving time and system time
    The scatter plot helps to better understand the meaning of bit/small covariance/correlation.
    For every rho, two scatter plots are needed.
    The simulation parameters are the same as in task_4_3_1()
    """
    plt.rcParams["figure.figsize"] = (20, 20)
    sim_param = SimParam()
    sim_param.SIM_TIME = 10000000
    sim_param.NUM_USERS = 2
    sim_param.NUM_SERVERS = 1
    sim_param.SERVERS_SEEDS = [100]
    sim_param.USERS_SEEDS = [i for i in range(sim_param.NUM_USERS)]
    sim_param.SERVICE_RATES = [0.015]
    sim_param.S = 10000
    sim_param.ARRIVAL_RATES = [0.015 for _ in range(sim_param.NUM_USERS)]
    sim_param.USERS_ARRIVAL_PROCESS = ARR_PROCESS.EXPONENTIAL

    sim = Simulation(sim_param)

    plot_id = 1
    for lam in [0.015 / 200, 0.015 / 4, 0.015 * 0.8 / 2, 0.015 * 0.95 / 2]:
        sim_param.ARRIVAL_RATES = [lam for _ in range(sim_param.NUM_USERS)]
        sim.reset()
        sim.do_simulation()

        iat = sim.statistics_collection.cnt_iat_st.x.values
        service_time = sim.statistics_collection.cnt_iat_st.y.values
        system_time = sim.statistics_collection.cnt_iat_syst.y.values

        # Plot iat vs. service time
        plt.subplot(int("42%d" % plot_id))
        plot_id += 1
        plt.title(r"$\rho$=" + str(lam/0.015*2))

        plt.xlabel("inter-arrival time")
        plt.ylabel("service time")
        plt.scatter(iat, service_time, marker="+", color="red")

        # Plot service time vs. system time
        plt.subplot(int("42%d" % plot_id))
        plot_id += 1
        plt.title(r"$\rho$=" + str(lam/0.015*2))

        plt.xlabel("service time")
        plt.ylabel("system time")
        plt.scatter(service_time, system_time, marker="+")
    plt.show()


def task_4_3_3():
    """
    Exercise to plot auto correlation depending on lags. Run simulation until 10000 (or 100) packets are served.
    For the different rho values, simulation is run and the blocking probability is auto correlated.
    Results are plotted for each N value in a different diagram.
    Note, that for some seeds with rho=0.DES and N=100, the variance of the auto covariance is 0 and returns an error.
    """
    plt.rcParams["figure.figsize"] = (20, 10)
    sim_param = SimParam()
    sim_param.SIM_TIME = 10000000
    sim_param.NUM_USERS = 2
    sim_param.NUM_SERVERS = 1
    sim_param.SERVERS_SEEDS = [100]
    sim_param.USERS_SEEDS = [i for i in range(sim_param.NUM_USERS)]
    sim_param.SERVICE_RATES = [0.015]
    sim_param.S = 10000
    sim_param.ARRIVAL_RATES = [0.015 for _ in range(sim_param.NUM_USERS)]
    sim_param.USERS_ARRIVAL_PROCESS = ARR_PROCESS.EXPONENTIAL

    sim = Simulation(sim_param)

    n = 100
    for lam in [0.015 / 200, 0.015 / 4, 0.015 * 0.8 / 2, 0.015 * 0.95 / 2]:
        sim_param.ARRIVAL_RATES = [lam for _ in range(sim_param.NUM_USERS)]
        sim.reset()
        sim.do_simulation_n_limit(n)

        lag = []
        cor = []

        for i in range(20):
            c = sim.statistics_collection.acnt_wt.get_auto_cor(i + 1)
            lag.append(i + 1)
            cor.append(c)

        plt.subplot(121)
        plt.plot(lag, cor, "-o", label="rho = " + str(lam/0.015*2))

    plt.subplot(121)
    plt.xlabel("lag")
    plt.ylabel("autocorrelation")
    plt.legend(loc='upper right')
    plt.title("N=" + str(n))

    n = 10000
    for lam in [0.015 / 200, 0.015 / 4, 0.015 * 0.8 / 2, 0.015 * 0.95 / 2]:
        sim_param.ARRIVAL_RATES = [lam for _ in range(sim_param.NUM_USERS)]
        sim.reset()
        sim.do_simulation_n_limit(n)

        lag = []
        cor = []

        for i in range(20):
            c = sim.statistics_collection.acnt_wt.get_auto_cor(i + 1)
            lag.append(i + 1)
            cor.append(c)

        plt.subplot(122)
        plt.plot(lag, cor, "-o", label="rho = " + str(lam/0.015*2))

    plt.subplot(122)
    plt.xlabel("lag")
    plt.ylabel("autocorrelation")
    plt.legend(loc='upper right')
    plt.title("N=" + str(n))
    plt.show()

if __name__ == '__main__':
    #task_4_2_1()
    task_4_3_1()
    #task_4_3_2()
    #task_4_3_3()