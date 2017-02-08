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

    ####################
    # HELPER FUNCTIONS #
    ####################
    
    def read_input(self):
        input_list = None
        for l in [line.strip('\n') for line in self.infile]:
            input_list = l.split(' ')
            
        pid = 0
        for i in range(0, len(input_list), 2):
            self.processes.append(Process(pid, int(input_list[i]), int(input_list[i+1])))
            pid += 1
        self.process_count = len(self.processes)
        self.infile.close()
        
        # for p in self.processes:
        #     print(p.arrival, p.runtime)
    
    ####################
    # PUBLIC FUNCTIONS #
    ####################
    
    def run(self):
        self.read_input()
        fifo = FIFO(self.processes, self.process_count)
        sjf = SJF(self.processes, self.process_count)
        print(fifo.output())
        print(sjf.output())
        
    
    
