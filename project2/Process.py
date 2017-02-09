class Process:
    def __init__(self, pid, arrival, runtime):
        self.arrival = arrival
        self.runtime = runtime
        self.remaining_time = runtime
        self.pid = pid
        
    def __lt__(self, other):
        return self.remaining_time < other.remaining_time
        
    def __gt__(self, other):
        return self.remaining_time > other.remaning_time
        
    def __eq__(self, other):
        return self.remaining_time == other.remaining_time