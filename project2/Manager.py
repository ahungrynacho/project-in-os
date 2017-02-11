from FIFO import FIFO
from SJF import SJF
from SRT import SRT
from MLF import MLF
from Process import Process

class Manager:
    def __init__(self, infile, expected_output):
        self.infile = open(infile, 'r')
        self.processes = []
        self.process_count = 0

    ###########
    # PRIVATE #
    ###########
    
    def read_input(self):
        """ Reads a 1-line plain text file and populates a list with Process(). """
        input_list = None
        for l in [line.strip('\n') for line in self.infile]:
            input_list = l.split(' ')
            
        pid = 0
        for i in range(0, len(input_list), 2):
            self.processes.append(Process(pid, int(input_list[i]), int(input_list[i+1])))
            pid += 1
        self.process_count = len(self.processes)
        self.infile.close()
    
    ##########
    # PUBLIC #
    ##########
    
    def run(self):
        self.read_input()
        
        sched_algs = [
            FIFO(self.processes, self.process_count), 
            SJF(self.processes, self.process_count),
            SRT(self.processes, self.process_count),
            MLF(self.processes, self.process_count)
            ]
        
        for alg in sched_algs:
            print(alg.output())
        
    
    
