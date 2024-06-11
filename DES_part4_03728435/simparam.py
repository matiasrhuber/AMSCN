from dataclasses import dataclass, field
from enum import Enum

class ARR_PROCESS(Enum):
    UNIFORM = 1
    EXPONENTIAL = 2

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

    # DONE Task 2.3:
    #######################################
    # number of users (customers) and their arrival rates in packets/ms
    NUM_USERS: int = 1
    ARRIVAL_RATES: list = field(default_factory=lambda: [0.0015])

    # number of servers and their service rates in packets/ms
    NUM_SERVERS: int = 1
    SERVICE_RATES: list = field(default_factory=lambda: [0.0015])
    #######################################

    USERS_SEEDS: list = field(default_factory=lambda: [None])
    SERVERS_SEEDS: list = field(default_factory=lambda: [None])

    USERS_ARRIVAL_PROCESS = ARR_PROCESS.EXPONENTIAL





