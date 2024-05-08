from dataclasses import dataclass


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

    # arrival rate of user in packets/ms
    ARRIVAL_RATE: int = 0.002

    # service rate of server in packets/ms
    SERVICE_RATE: int = 0.0015






