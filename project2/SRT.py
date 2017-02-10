from Scheduler import Scheduler
from heapq import *
class SRT(Scheduler):
    """ Shortest Remaining Time """
    def __init__(self, processes, process_count):
        Scheduler.__init__(self, processes, process_count)
        self.heap = [] # elements are Process()
    
    ###########
    # PRIVATE #
    ###########
    
    def execute(self):
        """ Uses a min-heap to determine the real-time of each process. """
        self.fill_table(self.processes)
        self.sort_table()
        for i in range(0, self.max_real_time+1, 1):
            self.timer = i
            if i in self.h_table.keys():
                for p in self.h_table[i]:
                    heappush(self.heap, p)
                
            if len(self.heap) and self.heap[0].remaining_time == 0:
                p = heappop(self.heap)
                real_time = self.timer - p.arrival
                self.total_real_time += real_time
                self.rt_table[p.pid] = real_time
            
            if (len(self.heap)):
                self.heap[0].remaining_time -= 1
                heapify(self.heap)
                # print([("pid:" + str(p.pid), "time remaning:" + str(p.remaining_time)) for p in self.heap])
                
        return
    
    ##########
    # PUBLIC #
    ##########
    def output(self):
        """ Returns a string containing the real-time of each process. """
        result = ""
        self.execute()
        for pid in sorted(self.rt_table.keys()):
            result += " " + str(self.rt_table[pid])
            
        result = "{:.2f}{}".format(self.average(self.total_real_time, self.process_count), result)
        return result