class Process:
    def __init__(self, pid, arrival, runtime):
        self.arrival = arrival
        self.runtime = runtime
        self.remaining_time = runtime
        self.pid = pid
        