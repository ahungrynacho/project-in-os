from Scheduler import Scheduler
class SJF(Scheduler):
    """ Shortest Job First """
    def __init__(self, processes, process_count):
        Scheduler.__init__(self, processes, process_count)
        self.queue = []
        self.current_process = None
    
    ##########    
    # PUBLIC #
    ##########
    def execute(self):
        """ Returns the real-time of the given process. """
        self.fill_table(self.processes, self.h_table)
        self.sort_table(self.h_table)
        
        for i in range(0, self.end_time, 1):
            self.timer = i

            if self.current_process != None and self.current_process.remaining_time == 0:
                real_time = self.timer - self.current_process.arrival
                self.total_real_time += real_time
                self.rt_table[self.current_process.pid] = real_time
                self.queue.remove(self.current_process)
            
            if i in self.h_table.keys():
                self.queue += self.h_table[i]
                
            if len(self.queue):
                self.current_process = self.queue[0]
                
            if self.current_process != None:
                self.current_process.remaining_time -= 1            
            
        return
    
