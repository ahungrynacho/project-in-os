from decimal import *
class Scheduler:
    """ abstract parent class """
    def __init__(self, processes, process_count):
        self.processes = processes # list of Process()
        self.process_count = process_count
        self.total_real_time = 0
        self.avg_turnaround = 0
        self.timer = 0
        DefaultContext.rounding = ROUND_DOWN
    
    def average(self, total_real_time, process_count):
        return Decimal(total_real_time) / Decimal(process_count)
        