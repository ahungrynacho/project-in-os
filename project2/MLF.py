from Scheduler import Scheduler
class MLF(Scheduler):
    """ Multi-level Feedback """
    def __init__(self, processes, process_count):
        Scheduler.__init__(self, processes, process_count)
        self.levels = dict() # (time quantum per process : (pid : total execution time of the current level))
        
        
    def output_levels(self):
        result = ""
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
        self.h_table[process.pid] = real_time
        self.h_table[clock].remove(process)
        return
    
    def run(self, clock):
        for p in self.h_table[clock]:
            level = self.find_level(p.pid)
            if level:
                self.levels[level][p.pid] += 1
                p.remaining_time -= 1
                
            if p.remaining_time == 0:
                self.terminate(clock, p)
            break
        return
    
    def execute(self):
        self.fill_table(self.processes)
        self.init_levels()
        
        for i in range(0, self.max_real_time+1, 1):
            self.timer = i
            if i in self.h_table.keys():
                self.run(i)
            elif len(self.h_table.keys()):
                self.run(sorted(self.h_table.keys())[0])
            
            # if i in self.h_table.keys():
            #     for p in self.h_table[i]:
            #         level = self.find_level(p.pid)
            #         if level:
            #             self.levels[level][p.pid] += 1
            #             p.remaining_time -= 1
                        
            #             if p.remaining_time == 0:
            #                 real_time = self.timer - p.arrival
            #                 self.total_real_time += real_time
            #                 self.rt_table[p.pid] = real_time
            #                 self.h_table[i].remove(p)
                        
            #             break
        print(self.output_levels())
        return
    
    def output(self):
        """ Returns a string containing the real-time of each process. """
        result = ""
        self.execute()
        for pid in sorted(self.rt_table.keys()):
            result += " " + str(self.rt_table[pid])
            
        result = "{:.2f}{}".format(self.average(self.total_real_time, self.process_count), result)
        return result