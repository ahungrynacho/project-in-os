from Scheduler import *
class MLF(Scheduler):
    """ Multi-level Feedback """
    def __init__(self, processes, process_count):
        Scheduler.__init__(self, processes, process_count)
        self.cqueue = [] # elements are Process()
        self.cq_index = 0 # current index of the circular queue
        self.current_process = None

        self.levels = dict() # (time quantum per process : (pid : total execution time of the current level))

    ###########
    # PRIVATE #
    ###########
    
    def output_levels(self):
        """ Returns a string with the contents of self.levels. """
        result = "(level : (pid : total execution time of the current level))\n"
        for level in sorted(self.levels):
            result += "{} : {}\n".format(str(level), str([(str(pid)) + " : " + str(self.levels[level][pid]) for pid in self.levels[level]]))
        return result
        
    def output_cqueue(self):
        """ Returns a string with the pid, remaining time and runtime of each process in the circular queue. """
        result = "(pid, remaining time, runtime)\n"
        for p in self.cqueue:
            result += "({}, {}, {}) ".format(p.pid, p.remaining_time, p.runtime)
        return result
        
    def find_level(self, pid):
        """ Returns the first level with space for the process to occupy a time quantum. """
        for level in sorted(self.levels.keys()): # levels: 1, 2, 4, 8, 16
            if pid not in self.levels[level].keys():
                self.levels[level][pid] = 0
                return level
            elif self.levels[level][pid] < level:
                return level
                
        return -1
        
    def init_levels(self):
        """ Initializes the levels. """
        for n in range(0, 5):
            self.levels[2 ** n] = dict()
        return
    
    def terminate(self, clock, process):
        """ Records the real-time of a process and removes it from the circular queue. """
        real_time = clock - process.arrival
        self.total_real_time += real_time
        self.rt_table[process.pid] = real_time
        self.cqueue.remove(process)
        return
    
    def execute(self):
        """ Runs the multi-level feedback algorithm. """
        self.fill_table(self.processes, self.h_table)
        self.init_levels()
        
        for i in range(0, self.max_real_time+1, 1):
            self.timer = i
            level = None
            
            if self.current_process != None:
                level = self.find_level(self.current_process.pid)
                self.levels[level][self.current_process.pid] += 1
                self.current_process.remaining_time -= 1 

            if self.current_process != None and self.current_process.remaining_time == 0:
                self.terminate(self.timer, self.current_process)
            elif self.current_process != None:  
                self.cq_index += 1
                
            if self.cq_index >= len(self.cqueue): # wrap around
                self.cq_index = 0
                
            if i in self.h_table.keys(): # preempt the current process with new processes
                self.cq_index = len(self.cqueue)
                self.cqueue += self.h_table[i]
                
            if len(self.cqueue) > 0:
                self.current_process = self.cqueue[self.cq_index]
              
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