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
        self.h_table = dict() # (int arrival : [Process])
        self.rt_table = dict() # (int pid : int real_time)
    
    def average(self, total_real_time, process_count):
        """ Returns the average turn-around time of the child class's scheduling algorithm. """
        return Decimal(total_real_time) / Decimal(process_count)
        
    def fill_table(self, processes):
        """ Populates a hash table with keys as arrival times corresponding with values as processes. """
        for p in processes:
            if p.arrival not in self.h_table:
                self.h_table[p.arrival] = []
            self.h_table[p.arrival].append(p)
            
        return
    
    def sort_table(self):
        """ Sorts the values, a list of Process(), of self.h_table in ascending runtime order. """
        for key in self.h_table:
            self.h_table[key].sort(key=lambda p: p.runtime)
        return
    
        