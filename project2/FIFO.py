from Scheduler import Scheduler

class FIFO(Scheduler):
    """ First-in, First-out """
    def __init__(self, processes, process_count):
        Scheduler.__init__(self, processes, process_count)
        
    def execute(self, process):
        self.timer += process.runtime
        real_time = self.timer - process.arrival
        return real_time
        
    def output(self):
        result = ""
        for p in self.processes:
            real_time = self.execute(p)
            self.total_real_time += real_time
            result += " " + str(real_time)
        
        result = "{:.2f}{}".format(self.average(self.total_real_time, self.process_count), result)
        return result