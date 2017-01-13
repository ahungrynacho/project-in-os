from rcb import ResourceControlBlock, BlockedError
from pcb import ProcessControlBlock

class Manager:
    def __init__(self):
        self.ready_list = [[] for x in range(0, 3)]
        self.blocked_list = [[] for x in range(0, 3)]
        self.resources = []
        self.ready_list[0].append(ProcessControlBlock("init", self.resources, "running", self.ready_list, None, 0))
        self.curr_proc = self.ready_list[0][0]
        
        for i in range(1, 5):
            rids = ['_', "R1", "R2", "R3", "R4"]
            self.resources.append(ResourceControlBlock(rids[i], i))
            
    ####################        
    # helper functions #
    ####################
    
    def list_processes(self, proc_list):
        result = "{:12}{:12}{}\n".format("Process", "Priority", "Status")
        for priority in proc_list:
            for proc in priority:
                result += "{:12}{:12}{}\n".format(proc.pid, str(proc.priority), proc.status)
                
        return result
        
    def list_resources(self):
        result = "{:12}{:12}{:12}{:20}{:20}\n".format("Resource", "Total", "Available", "Waiting List", "Consumer List")
        for rcb in self.resources:
            result += "{:12}{:12}{:12}{:20}{:20}\n".format(
                                                        rcb.rid, str(rcb.total), str(rcb.available), 
                                                        str([ pcb.pid for pcb in rcb.waiting_list]),
                                                        str([ (pcb.pid, rcb.consumer_map[pcb]) for pcb in rcb.consumer_map])
                                                    )
        return result
        
    def del_tree(self, proc):
        if len(proc.pcb_children) == 0:
            for p in self.ready_list[proc.priority]:
                if proc.pid == p.pid:
                    self.ready_list[proc.priority].remove(p)
                    return
        
        for child in proc.pcb_children:
            self.del_tree(child)
        
        self.ready_list[proc.priority].remove(proc)
        if proc == self.curr_proc:
            self.curr_proc = None

        return    
    
    ##################
    # main functions #
    ##################
    
    def scheduler(self):
        for i in range (2, -1, -1):
            for proc in self.ready_list[i]:
                if self.curr_proc == None or proc.priority > self.curr_proc.priority or self.curr_proc.status != "running":
                    self.curr_proc = proc
                    self.curr_proc.status = "running"
                    return
    
    def cr(self, pid, priority):
        new_proc = ProcessControlBlock(pid, self.resources, "ready", self.ready_list, self.curr_proc, priority)
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
        root = None
        for row in self.ready_list:
            for proc in row:
                if proc.pid == pid:
                    root = proc
                    break
                
        self.del_tree(root)
        self.scheduler()
        return
    
    def to(self):
        self.curr_proc.status = "ready"
        self.ready_list[self.curr_proc.priority].remove(self.curr_proc)
        self.ready_list[self.curr_proc.priority].append(self.curr_proc)
        self.scheduler()
        # self.ready_list[self.curr_proc.priority][0].status = "running"
        # self.curr_proc = self.ready_list[self.curr_proc.priority][0]
        
        return
    
    
    def req(self, rid, amount):
        for rcb in self.resources:
            if rcb.rid == rid:
                try:
                    if self.curr_proc not in rcb.consumer_map:
                        rcb.consumer_map[self.curr_proc] = rcb.req(amount)
                    else:
                        rcb.consumer_map[self.curr_proc] += rcb.req(amount)
                        
                except BlockedError:
                    self.curr_proc.status = "blocked"
                    self.ready_list[self.curr_proc.priority].remove(self.curr_proc)
                    self.blocked_list[self.curr_proc.priority].append(self.curr_proc)
                    rcb.waiting_list.append(self.curr_proc)
                    self.scheduler()
                    
                except ValueError:
                    print "ERROR"
                    
        return
    
    def rel(self, rid, amount):
        return
    
    
if __name__ == "__main__":
    
    manager = Manager()
    manager.cr('A', 1)
    manager.cr('B', 1)
    manager.cr('C', 2)
    manager.cr('D', 1)
    manager.cr('E', 1)
    # manager.to()
    print manager.list_processes(manager.ready_list)
    manager.de('C')
    print manager.list_processes(manager.ready_list)
    manager.req("R4", 3)
    manager.req("R4", 3)
    manager.req("R4", 3)
    print manager.list_resources()
    print manager.list_processes(manager.ready_list)
    print manager.list_processes(manager.blocked_list)
            