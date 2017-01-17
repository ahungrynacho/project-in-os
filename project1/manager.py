from rcb import ResourceControlBlock, BlockedError
from pcb import ProcessControlBlock, BlockedProcess

class Manager:
    def __init__(self, infile):
        self.ready_list = [[] for x in range(0, 3)] # elements are ProcessControlBlock()
        self.blocked_list = [[] for x in range(0, 3)] # elements are ProcessControlBlock()
        self.process_list = [self.ready_list, self.blocked_list]
        self.resources = dict() # (rid : ResourceControlBlock())
        self.ready_list[0].append(ProcessControlBlock("init", "running", self.ready_list, None, 0))
        self.curr_proc = self.ready_list[0][0]
        
        self.infile = open(infile, 'r')
        self.lines = [line for line in self.infile]
        self.infile.close()

        for i in range(1, 5):
            rids = ['_', "R1", "R2", "R3", "R4"]
            self.resources[rids[i]] = ResourceControlBlock(rids[i], i)
            
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
        
    def unblock(self, rid):
        rcb = self.resources[rid]
        if rcb.peek().amount <= rcb.available:
            unblk_proc = rcb.dequeue()
            rcb.req(unblk_proc.process.pid, unblk_proc.amount)
            self.blocked_list[unblk_proc.process.priority].remove(unblk_proc.process)
            self.ready_list[unblk_proc.process.priority].append(unblk_proc.process)
            return
    
    def del_tree(self, proc):
        if proc == None:
            return
        
        if proc == self.curr_proc:
            self.curr_proc = None
        
        if len(proc.pcb_children) == 0: # remove leaf nodes
            for p in self.ready_list[proc.priority]:
                if proc.pid == p.pid:
                    for rid in proc.resource_map: # release resources
                        self.rel(rid, proc.resource_map[rid])
                        # self.unblock(rid)
                        # self.clear_waiting_list(proc.pid)
                            
                    self.ready_list[proc.priority].remove(p)
                    # self.blocked_list[proc.priority].remove(p)
                    return
        
        for child in proc.pcb_children:
            self.del_tree(child)
            
        # for p in self.ready_list[proc.priority]: 
        #     if proc.pid == p.pid:
        #         self.ready_list[proc.priority].remove(p)
        self.ready_list[proc.priority].remove(proc) # remove the root

        return
    
    def is_blocked(self, pid):
        for rid in self.resources:
            for blocked_pcb in self.resources[rid].waiting_list:
                if blocked_pcb.process.pid == pid:
                    return True
        return False
        
    def clear_waiting_list(self, pid):
        for rid in self.resources:
            for blocked_proc in self.resources[rid].waiting_list:
                if blocked_proc.process.pid == pid:
                    self.resources[rid].waiting_list.remove(blocked_proc)
                    break
        return
    ##################
    # main functions #
    ##################
    
    def init(self):
        """ Restores system to its initial state """
        for priority in self.ready_list:
            del priority[:]
            
        for priority in self.blocked_list:
            del priority[:]
            
        for rid in self.resources:
            self.resources[rid].reset()
            
        self.ready_list[0].append(ProcessControlBlock("init", "running", self.ready_list, None, 0))
        self.curr_proc = self.ready_list[0][0]
            
                
    def scheduler(self):
        for i in range (2, -1, -1):
            for proc in self.ready_list[i]:
                if self.curr_proc == None or proc.priority > self.curr_proc.priority or self.curr_proc.status != "running":
                    self.curr_proc = proc
                    self.curr_proc.status = "running"
                    return
            # for proc in self.blocked_list[i]:
            #     if self.curr_proc == None or proc.priority > self.curr_proc.priority or self.curr_proc.status != "running":
            #         self.curr_proc = proc
            #         self.curr_proc.status = "running"
            #         self.blocked_list[i].remove(proc)
            #         self.clear_waiting_list(proc.pid)
            #         self.ready_list[i].insert(0, proc)
            #         return
    
    def cr(self, pid, priority):
        new_proc = ProcessControlBlock(pid, "ready", self.ready_list, self.curr_proc, priority)
        self.ready_list[priority].append(new_proc)
        self.curr_proc.pcb_children.append(new_proc)
        self.curr_proc.status = "ready"
        self.scheduler()
        # if new_proc.priority > self.curr_proc.priority:
        #     self.curr_proc.status = "ready"
        #     self.curr_proc = new_proc
        #     self.curr_proc.status = "running"
        
        return self.curr_proc.pid
        
    def de(self, pid):
        # for proc_list in self.process_list:
        for priority_row in self.ready_list:
            for proc in priority_row:
                if proc.pid == pid:
                    self.del_tree(proc)
                    proc.pcb_parent.pcb_children.remove(proc)
                    self.scheduler()
                    return
                
        return

    def to(self):
        self.curr_proc.status = "ready"
        self.ready_list[self.curr_proc.priority].remove(self.curr_proc)
        self.ready_list[self.curr_proc.priority].append(self.curr_proc)
        self.scheduler()
        return
    
    def req(self, proc, rid, amount):
        for RID in self.resources:
            if RID == rid:
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
    
    def rel(self, rid, amount):
        for RID in self.resources:
            rcb = self.resources[RID]
            if rcb.rid == rid:
                rcb.rel(amount)
                
                if len(rcb.waiting_list) != 0:
                    blocked_proc = rcb.waiting_list[0]
                    try:
                        if blocked_proc.process.pid not in rcb.consumer_map:
                            rcb.consumer_map[blocked_proc.process.pid] = rcb.req(blocked_proc.process.pid, blocked_proc.amount)
                        else:
                            rcb.consumer_map[blocked_proc.process.pid] += rcb.req(blocked_proc.process.pid, blocked_proc.amount)
                        blocked_proc.process.resource_map[rid] = blocked_proc.amount
                    
                    except BlockedError:
                        pass # remain in the blocked state
                    
                    else:
                        rcb.waiting_list.remove(blocked_proc)
                        
                        if not self.is_blocked(blocked_proc.process.pid):
                            self.blocked_list[blocked_proc.process.priority].remove(blocked_proc.process)
                        
    def run(self):
        result = "init "
        for line in self.lines:
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
                        self.rel(args[1], int(args[2]))
                    elif args[0] == "to":
                        self.to()
                    elif args[0] == "break":
                        break
                    
                except ValueError:
                    result += "error "
                else:
                    result += self.curr_proc.pid + " "
            else:
                result += "\n"
    
        return result