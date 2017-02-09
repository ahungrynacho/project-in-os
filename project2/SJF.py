from Scheduler import Scheduler
class SJF(Scheduler):
    """ Shortest Job First """
    def __init__(self, processes, process_count):
        Scheduler.__init__(self, processes, process_count)
    
    def execute(self, process):
        self.timer += process.runtime
        real_time = self.timer - process.arrival
        return real_time
        
    def output(self):
        result = ""
        self.fill_table(self.processes)
        for key in sorted(self.h_table.keys()):
            for p in self.h_table[key]:
                real_time = self.execute(p)
                self.total_real_time += real_time
                self.rt_table[p.pid] = real_time

        for pid in sorted(self.rt_table.keys()):
            result += " " + str(self.rt_table[pid])

        result = "{:.2f}{}".format(self.average(self.total_real_time, self.process_count), result)
        return result