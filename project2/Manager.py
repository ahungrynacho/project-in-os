from FIFO import FIFO
from SJF import SJF
from SRT import SRT
from MLF import MLF
from Process import Process

class Manager:
    def __init__(self):
        self.infile = None
        self.outfile = None
        self.testfile = None
        self.output = []
        self.exp_output = []
        self.processes = []
        self.process_count = 0

    ###########
    # PRIVATE #
    ###########
    
    def read_input(self, infile):
        """ Reads a 1-line plain text file and populates a list with Process(). """
        self.infile = open(infile, 'r')
        input_list = None
        for l in [line.strip('\n') for line in self.infile]:
            input_list = l.split(' ')
            
        pid = 0
        for i in range(0, len(input_list), 2):
            self.processes.append(Process(pid, int(input_list[i]), int(input_list[i+1])))
            pid += 1
        self.process_count = len(self.processes)
        self.infile.close()
        return
    
    
        
    def write_output(self, outfile, string):
        self.outfile = open(outfile, 'w')
        self.outfile.write(string)
        self.outfile.close()
        return
    
    ##########
    # PUBLIC #
    ##########
    
    def test(self, test_cases):
        if test_cases != None:
            self.testfile = open(test_cases, 'r')
            for line in self.testfile:
                if line[0] != '\n' or line[0] != '#':
                    self.exp_output.append(line.strip('\n'))
            
            for i in range(0, len(self.exp_output)):
                if self.exp_output[i] != self.output[i]:
                    print("FAIL")
                else:
                    print("PASS")
        return
    
    def run(self, infile, outfile):
        if infile != None:
            self.read_input(infile)
        
        sched_algs = [
            FIFO(self.processes, self.process_count), 
            SJF(self.processes, self.process_count),
            SRT(self.processes, self.process_count),
            MLF(self.processes, self.process_count)
            ]
        
        result = ""
        for alg in sched_algs:
            temp = alg.output()
            self.output.append(temp)
            result += "{}\n".format(temp)
            print(temp)
        result = result[0:len(result)-1] # remove the trailing \n
        
        if outfile != None:
            self.write_output(outfile, result)
            
        return
            
        