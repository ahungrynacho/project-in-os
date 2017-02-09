from Scheduler import Scheduler
from heapq import *
class SRT(Scheduler):
    """ Shortest Remaining Time """
    def __init__(self, processes, process_count):
        Scheduler.__init__(self, processes, process_count)
        self.heap = []
    
    def execute(self):
        self.fill_table(self.processes)
        for i in range(0, self.max_real_time, 1):
            self.timer += i
            if i in self.h_table.keys():
                for p in self.h_table[i]:
                    heappush(self.heap, p)
                # print([p.pid for p in self.heap])
                self.heap[0].remaining_time -= 1
                if self.heap[0].remaining_time == 0:
                    print(self.heap[0].pid)
                    p = heappop(self.heap)
                    print([p.pid for p in self.heap])
                    real_time = self.timer - p.arrival
                    self.total_real_time += real_time
                    self.rt_table[p.pid] = real_time
        # print([p.pid for p in self.heap])
        return
    
    def output(self):
        result = ""
        self.execute()
        for pid in sorted(self.rt_table.keys()):
            result += " " + str(self.rt_table[pid])
            
        result = "{:.2f}{}".format(self.average(self.total_real_time, self.process_count), result)
        return result