from Scheduler import Scheduler
class MLF(Scheduler):
    """ Multi-level Feedback """
    def __init__(self, processes, process_count):
        Scheduler.__init__(self, processes, process_count)
        self.levels = dict() # (max execution time per process : (pid : total execution time of the current level))
        
        
    def execute(self, process):
        self.fill_table(self.processes)
        for n in range(0, 5):
            self.levels[2 ** n] = dict()
        
        for i in range(0, self.max_real_time+1, 1):
            self.timer = i
            if i in self.h_table.keys():
                pass
        
        return
    def output(self):
        return