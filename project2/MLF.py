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
        
    def output_term_time(self):
        """ Returns a string containing the termination times of each process. """
        result = "(pid, arrival time, termination time)\n"
        for p in self.processes:
            result += "({},{},{}) ".format(p.pid, p.arrival, p.term_time)
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
        
    def last_level_full(self, pid):
        for level in sorted(self.levels.keys(), reverse = True):
            if pid in self.levels[level].keys() and self.levels[level][pid] >= level:
                return True
            elif pid in self.levels[level].keys() and self.levels[level][pid] < level:
                return False
        
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

    ##########
    # PUBLIC #
    ##########   
    def execute(self):
        """ Runs the multi-level feedback algorithm. """
        self.fill_table(self.processes, self.h_table)
        self.init_levels()
        
        for i in range(0, self.end_time, 1):
            self.timer = i

            if self.current_process != None and self.current_process.remaining_time == 0:
                self.current_process.term_time = self.timer
                self.terminate(self.timer, self.current_process)

            if i in self.h_table.keys(): # preempt the current process with new processes
                self.cqueue = self.h_table[i] + self.cqueue  
                
            if len(self.cqueue):
                self.current_process = self.cqueue[0]                 
                
            if self.current_process != None:
                level = self.find_level(self.current_process.pid)
                self.levels[level][self.current_process.pid] += 1
                self.current_process.remaining_time -= 1
                
                if self.last_level_full(self.current_process.pid) and self.current_process.remaining_time > 0:
                    self.cqueue.append(self.cqueue.pop(0))
                
        return
    