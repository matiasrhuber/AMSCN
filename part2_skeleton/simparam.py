from dataclasses import dataclass, field


@dataclass
class SimParam(object):

    """
    Contains all important simulation parameters
    """

    # buffer spaces
    S: int = 4  # waiting queue length

    # simulation time in ms
    SIM_TIME: int = 100000

    # number of runs in experiment
    NUM_RUNS: int = 1000

    # TODO Task 2.3: comment these lines
    #######################################
    # arrival rate of user in packets/ms
    ARRIVAL_RATE: int = 0.002

    # service rate of server in packets/ms
    SERVICE_RATE: int = 0.0015
    #######################################

    # TODO Task 2.3: and uncomment these lines
    """
    #######################################
    # number of users (customers) and their arrival rates in packets/ms
    NUM_USERS: int = 1
    ARRIVAL_RATES: list = field(default_factory=lambda: [0.0015])

    # number of servers and their service rates in packets/ms
    NUM_SERVERS: int = 1
    SERVICE_RATES: list = field(default_factory=lambda: [0.0015])
    #######################################
    """




