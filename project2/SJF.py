from Scheduler import Scheduler
class SJF(Scheduler):
    """ Shortest Job First """
    def __init__(self, processes, process_count):
        Scheduler.__init__(self, processes, process_count)
        self.sjf_table = dict() # (int arrival : [Process])
        self.sjf_rt_table = dict() # (int pid : int real_time)
    
    ###########
    # PRIVATE #
    ###########
    def execute(self, process):
        """ Returns the real-time of the given process. """
        self.timer += process.runtime
        real_time = self.timer - process.arrival
        return real_time
    
    ##########    
    # PUBLIC #
    ##########
    def output(self):
        """ Returns a string containing the real-time of each process. """
        result = ""
        self.fill_table(self.processes, self.sjf_table)
        self.sort_table(self.sjf_table)
        for key in sorted(self.sjf_table.keys()):
            for p in self.sjf_table[key]:
                real_time = self.execute(p)
                self.total_real_time += real_time
                self.sjf_rt_table[p.pid] = real_time

        for pid in sorted(self.sjf_rt_table.keys()):
            result += " " + str(self.sjf_rt_table[pid])

        result = "{:.2f}{}".format(self.average(self.total_real_time, self.process_count), result)
        return result