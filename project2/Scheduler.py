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
        self.max_real_time = sum([p.runtime for p in self.processes])
        self.h_table = dict() # (arrival : [process])
        self.rt_table = dict() # (pid : real_time)
    
    def average(self, total_real_time, process_count):
        return Decimal(total_real_time) / Decimal(process_count)
        
    def fill_table(self, processes):
        for p in processes:
            if p.arrival not in self.h_table:
                self.h_table[p.arrival] = []
            self.h_table[p.arrival].append(p)
            
        for key in self.h_table:
            self.h_table[key].sort(key=lambda p: p.runtime)
        return
        
    
        