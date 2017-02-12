from Scheduler import *
from heapq import *
class SRT(Scheduler):
    """ Shortest Remaining Time """
    def __init__(self, processes, process_count):
        Scheduler.__init__(self, processes, process_count)
        self.heap = [] # elements are Process()
        # self.srt_table = dict() # (int arrival : [Process])
        # self.srt_rt_table = dict() # (int pid : int real_time)
    
    ##########
    # PUBLIC #
    ##########
    
    def execute(self):
        """ Uses a min-heap to determine the real-time of each process. """
        self.fill_table(self.processes, self.h_table)
        for i in range(0, self.end_time, 1):
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
                # heapify(self.heap)
                
        return