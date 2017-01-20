from rcb import ResourceControlBlock
from pcb import ProcessControlBlock, BlockedProcess 
from my_exceptions import *

class Manager:
    def __init__(self, infile, expected_output):
        self.ready_list = [[] for x in range(0, 3)] # elements are ProcessControlBlock()
        self.blocked_list = [[] for x in range(0, 3)] # elements are ProcessControlBlock()
        self.process_list = [self.ready_list, self.blocked_list]
        self.ready_list[0].append(ProcessControlBlock("init", "running", self.ready_list, None, 0))
        self.curr_proc = self.ready_list[0][0]
        
        self.resources = dict() # (rid : ResourceControlBlock())
        for i in range(1, 5):
            rids = ['_', "R1", "R2", "R3", "R4"]
            self.resources[rids[i]] = ResourceControlBlock(rids[i], i)        
        
        #################
        # reading files #
        #################
        
        self.input_lines = None
        self.expected_output = None
        
        if infile != None:
            self.infile = open(infile, 'r')
            self.input_lines = [line for line in self.infile]
            self.infile.close()
        
        if expected_output != None:
            self.infile_output = open(expected_output, 'r')
            self.expected_output = [line.strip("\n") for line in self.infile_output]
            self.infile_output.close()
        
        self.gen_output = []
        self.outfile = open("57641580.txt", 'w')
        self.test_cases = dict()

    ####################        
    # helper functions #
    ####################
    
    def list_processes(self, proc_list):
        result = "{:12}{:12}{:12}{:12}\n".format("Process", "Priority", "Status", "Children")
        for priority in proc_list:
            for proc in priority:
                result += "{:12}{:12}{:12}{:12}\n".format(proc.pid, str(proc.priority), proc.status, str([pcb.pid for pcb in proc.pcb_children]))
                
        return result
        
    def list_resources(self):
        result = "{:12}{:12}{:12}{:40}{:20}\n".format("Resource", "Total", "Available", "Waiting List", "Consumer List")
        for rid in self.resources:
            result += "{:12}{:12}{:12}{:40}{:20}\n".format(
                                                        rid, str(self.resources[rid].total), str(self.resources[rid].available), 
                                                        str([ (blk_pcb.process.pid, blk_pcb.amount) for blk_pcb in self.resources[rid].waiting_list]),
                                                        str([ (pid, self.resources[rid].consumer_map[pid]) for pid in self.resources[rid].consumer_map])
                                                    )
        return result
    
    def del_from_list(self, proc, proc_list):
        """ 
        Deletes a process from the given process list and release its resources. 
        Processes on the waiting list in each RCB acquire resources they are waiting for.
        Clears the given process from waiting lists on all RCBs.
        """
        proc_list[proc.priority].remove(proc)
        for rid in proc.resource_map:
            self.rel(proc.pid, rid, proc.resource_map[rid])

        self.clear_waiting_list(proc.pid)
        proc.pcb_parent.pcb_children.remove(proc)
        return
    
    def del_tree(self, proc):
        """ Recursively deletes a process and all its children while releasing resources held by its children."""
        if proc == None:
            return
        
        if proc == self.curr_proc:
            self.curr_proc = None
        
        # removing leaf nodes
        if len(proc.pcb_children) == 0: 
            if proc.status == "ready" or proc.status == "running":
                self.del_from_list(proc, self.ready_list)
            else:
                self.del_from_list(proc, self.blocked_list)
            return
        
        # recursive call
        for child in proc.pcb_children:
            self.del_tree(child)
        
        # removing the root
        if proc.status == "ready" or proc.status == "running":
            self.ready_list[proc.priority].remove(proc) 
        else:
            self.blocked_list[proc.priority].remove(proc)
        proc.pcb_parent.pcb_children.remove(proc)
        return
    
    def all_blocked(self, proc):
        """ If the given resource is on the waiting list in any RCB, return True otherwise return False. """
        for rid in self.resources:
            for blocked_pcb in self.resources[rid].waiting_list:
                if blocked_pcb.process.pid == proc.pid:
                    return True
        
        return False
        
    def is_unique(self, pid):
        """ Returns True if there are no duplicate processes in self.ready_list and/or self.block_list otherwise return False. """
        for proc_list in self.process_list:
            for priority_lvl in proc_list:
                for pcb in priority_lvl:
                    if pcb.pid == pid:
                        return False
        return True
        
    def clear_waiting_list(self, pid):
        """ Removes the given process from the waiting list of every RCB. """
        for rid in self.resources:
            for blocked_proc in self.resources[rid].waiting_list:
                if blocked_proc.process.pid == pid:
                    self.resources[rid].waiting_list.remove(blocked_proc)
                    break
        return
    
    def blocked_list_to_ready_list(self, proc):
        """ Moves the given process from self.blocked_list to self.ready_list. """
        for p in self.blocked_list[proc.priority]:
            if proc.pid == p.pid:
                self.ready_list[proc.priority].append(proc)
                self.blocked_list[proc.priority].remove(proc)
        return
    
    def ready_list_to_blocked_list(self, proc):
        """ Moves the given process from self.ready_list to self.blocked_list. """
        for p in self.ready_list[proc.priority]:
            if proc.pid == p.pid:
                self.blocked_list[proc.priority].append(proc)
                self.ready_list[proc.priority].remove(proc)
        return
    
    def remove_trailing_space(self, string):
        """ Removes the \n and trailing space when generating output in self.run(). """
        string.strip("\n")
        return string[0:len(string)-1]  
    
    ##################
    # main functions #
    ##################
    
    def init(self):
        """ Restores system to its initial state by clearing and resetting all data structures. """
        for priority in self.ready_list:
            del priority[:]
            
        for priority in self.blocked_list:
            del priority[:]
            
        for rid in self.resources:
            self.resources[rid].reset()
            
        self.ready_list[0].append(ProcessControlBlock("init", "running", self.ready_list, None, 0))
        self.curr_proc = self.ready_list[0][0]
        return
                
    def scheduler(self):
        """ Determines the next running process by checking self.ready_list. """
        
        for i in range(2, -1, -1):    
            for proc in self.ready_list[i]:
                if self.curr_proc == None or self.curr_proc.status == "blocked":
                    self.curr_proc = proc
                    self.curr_proc.status = "running"
                    return
                elif proc.priority > self.curr_proc.priority or self.curr_proc.status != "running":
                    self.curr_proc.status = "ready"
                    self.curr_proc = proc
                    self.curr_proc.status = "running"
                    return
        return None
    
    def cr(self, pid, priority):
        """ Creates a new process and appends it to the self.ready_list. """
        if not self.is_unique(pid):
            raise DuplicateProcessError
        elif priority == 0:
            raise ModifyingInitProcessError
        
        new_proc = ProcessControlBlock(pid, "ready", self.ready_list, self.curr_proc, priority)
        self.ready_list[priority].append(new_proc)
        self.curr_proc.pcb_children.append(new_proc)
        # self.curr_proc.status = "ready"
        self.scheduler()
        
        return self.curr_proc.pid
        
    def de(self, pid):
        """ 
        Deletes a process from the self.ready_list or the self.blocked_list.
        Removes the process from the parent's pcb_children list.
        """
        if pid == "init":
            raise ModifyingInitProcessError
            
        for proc_list in self.process_list:
            for priority_row in proc_list:
                for proc in priority_row:
                    if proc.pid == pid:
                        self.del_tree(proc)
                        self.scheduler()
                        return
                
        raise NonexistentObjectError

    def to(self):
        """ Moves the currently running process to the end of its queue in a circular round-robin fashion. """
        self.curr_proc.status = "ready"
        self.ready_list[self.curr_proc.priority].remove(self.curr_proc)
        self.ready_list[self.curr_proc.priority].append(self.curr_proc)
        self.scheduler()
        return
    
    def req(self, proc, rid, amount):
        """ If enough resources are available, rid's resources are granted to the currently running process. """
        try:
            self.resources[rid].req(proc.pid, amount)
            proc.resource_map[rid] = amount
                
        except BlockedError:
            proc.status = "blocked"
            self.ready_list[proc.priority].remove(proc)
            self.blocked_list[proc.priority].append(proc)
            self.resources[rid].waiting_list.append(BlockedProcess(proc, rid, amount))
            self.scheduler()
                    
        return
    
                
    def rel(self, pid, rid, amount):
        """ The currently running resource releases a specified amount of resources. """
        if self.curr_proc != None and self.curr_proc.pid == "init":
            raise ModifyingInitProcessError
            
        if rid in self.resources:
            rcb = self.resources[rid]
            rcb.rel(pid, amount)
            for proc in rcb.unblock():
                self.blocked_list_to_ready_list(proc)
            self.scheduler()
                    
        else:
            raise NonexistentObjectError
        return
    
    def test(self):
        """ Print out the test results by comparing the generated output with the expected output. """
        result = ""
        if self.expected_output != None:
            for i in range(0, len(self.expected_output), 1):
                if self.expected_output[i] == "break":
                    break
                elif self.gen_output[i] != self.expected_output[i]:
                    result += "FAIL: {}\n".format(self.test_cases[i])
                else:
                    result += "PASS: {}\n".format(self.test_cases[i])
        return result
    
    def run(self):
        """ Handler that parses commands from input.txt and generates output.txt. """
        test_num = 0
        result = "init "
        for line in self.input_lines:
            args = line.split()
            if len(args) > 0:
                try:
                    if args[0] == "init":
                        self.init()
                    elif args[0] == "cr":
                        self.cr(args[1], int(args[2]))
                    elif args[0] == "de":
                        self.de(args[1])
                    elif args[0] == "req":
                        self.req(self.curr_proc, args[1], int(args[2]))
                    elif args[0] == "rel":
                        self.rel(self.curr_proc.pid, args[1], int(args[2]))
                    elif args[0] == "to":
                        self.to()
                    elif args[0] == "#":
                        self.test_cases[test_num] = " ".join(args[1:])
                        test_num += 1
                        continue
                    elif args[0] == "break":
                        break
                    
                except (ValueError, BlockedError, DuplicateProcessError, NonexistentObjectError, ModifyingInitProcessError) as e:
                    result += "error "
                else:
                    result += self.curr_proc.pid + " "
            else:
                result += "\n"
        
        for line in result.split("\n"):
            self.gen_output.append(self.remove_trailing_space(line))
            line = line + "\n"
            self.outfile.write(line)
        self.outfile.close()
        return result