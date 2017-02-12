from decimal import *
from copy import deepcopy
class Scheduler:
    """ abstract parent class """
    def __init__(self, processes, process_count):
        # Primitive data types are implicitly passed by value.
        self.process_count = process_count
        self.total_real_time = 0
        self.avg_turnaround = 0
        self.timer = 0
        DefaultContext.rounding = ROUND_DOWN
        
        # Objects are implicitly passed by reference.
        self.h_table = dict() # (int arrival : [Process])
        self.rt_table = dict() # (int pid : int real_time)
        self.processes = deepcopy(processes) # list of Process()
        self.max_real_time = sum([p.runtime for p in self.processes])
    
    def average(self, total_real_time, process_count):
        """ Returns the average turn-around time of the child class's scheduling algorithm. """
        return Decimal(total_real_time) / Decimal(process_count)
        
    def fill_table(self, processes, h_table):
        """ Populates a hash table with keys as arrival times corresponding with values as processes. """
        for p in processes:
            if p.arrival not in h_table:
                h_table[p.arrival] = []
            h_table[p.arrival].append(p)
            
        return
    
    def sort_table(self, h_table):
        """ Sorts the values, a list of Process(), of self.h_table in ascending runtime order. """
        for key in h_table:
            h_table[key].sort(key=lambda p: p.runtime)
        return
    
    def output_htable(self, h_table):
        """ Returns a string containing a list of processes corresponding to each arrival time. """
        result = "(arrival : [(pid, remaining time, runtime)]\n"
        for key in h_table.keys():
            result += "({} : {})\n".format(key, str([(p.pid, p.remaining_time, p.runtime) for p in h_table[key]]))
        return result
    
        