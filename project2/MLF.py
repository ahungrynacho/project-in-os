from Scheduler import *
class MLF(Scheduler):
    """ Multi-level Feedback """
    def __init__(self, processes, process_count):
        Scheduler.__init__(self, processes, process_count)
        self.cqueue = [] # elements are Process()
        self.cq_index = 0 # current index of the circular queue
        self.current_process = None

        self.levels = dict() # (time quantum per process : (pid : total execution time of the current level))
        self.mlf_table = dict() # (int arrival : [Process])
        self.mlf_rt_table = dict() # (int pid : int real_time)
        
    def output_levels(self):
        result = "(level : (pid : total execution time of the current level))\n"
        for level in sorted(self.levels):
            result += "{} : {}\n".format(str(level), str([(str(pid)) + " : " + str(self.levels[level][pid]) for pid in self.levels[level]]))
        return result
        
    def find_level(self, pid):
        """ 
        Returns the first level with space for the process to occupy a time quantum.
        """
        for level in sorted(self.levels.keys()): # levels: 1, 2, 4, 8, 16
            if pid not in self.levels[level].keys():
                self.levels[level][pid] = 0
                return level
            elif self.levels[level][pid] < level:
                return level
                
        return -1
        
    def init_levels(self):
        for n in range(0, 5):
            self.levels[2 ** n] = dict()
        return
    
    def terminate(self, clock, process):
        real_time = clock - process.arrival
        self.total_real_time += real_time
        self.mlf_rt_table[process.pid] = real_time
        self.cqueue.remove(process)
        return
    
    def output_cqueue(self):
        result = "(pid, remaining time, runtime)\n"
        for p in self.cqueue:
            result += "({}, {}, {}) ".format(p.pid, p.remaining_time, p.runtime)
        return result
            
    def execute(self):
        self.fill_table(self.processes, self.mlf_table)
        self.init_levels()
        print(self.output_htable(self.mlf_table))
        
        for i in range(0, self.max_real_time+1, 1):
            self.timer = i
            if i in self.mlf_table.keys():
                self.cq_index = len(self.cqueue)
                self.cqueue += self.mlf_table[i]
                print(self.output_cqueue())
                self.current_process = self.cqueue[self.cq_index]
                
            
            # print("(pid, remaining time) " + str((self.cqueue[self.cq_index].pid, self.cqueue[self.cq_index].remaining_time)))
            # print("(pid, remaining time) " + str((self.current_process.pid, self.current_process.remaining_time)))
            self.current_process.remaining_time -= 1
            level = self.find_level(self.current_process.pid)
            if level:
                self.levels[level][self.current_process.pid] += 1
                
            if self.current_process.remaining_time == 0:
                print("terminating processs: " + str(self.current_process.pid))
                self.terminate(self.timer, self.current_process)
                self.cq_index -= 1 # compensate for deleting an element in the middle of the queue
                
            self.cq_index += 1
            if self.cq_index >= len(self.cqueue):
                self.cq_index = 0
            self.current_process = self.cqueue[self.cq_index]
                
        print(self.output_levels())
        return
    
    def output(self):
        """ Returns a string containing the real-time of each process. """
        result = ""
        self.execute()
        print(self.total_real_time)
        
        for pid in sorted(self.mlf_rt_table.keys()):
            result += " " + str(self.mlf_rt_table[pid])
            
        result = "{:.2f}{}".format(self.average(self.total_real_time, self.process_count), result)
        return result