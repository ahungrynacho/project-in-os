from my_exceptions import BlockedError, ModifyingInitProcessError, NonexistentObjectError
class ResourceControlBlock:
    def __init__(self, rid, total):
        self.rid = rid
        self.total = total
        self.available = total
        self.consumed = self.total - self.available
        self.waiting_list = [] # elements are BlockedProcess()
        self.consumer_map = dict() # (pid : amount)
    
    ####################
    # helper functions #
    ####################
    
    def peek(self):
        if len(self.waiting_list) > 0:
            return self.waiting_list[0]
        else:
            return None
            
    def dequeue(self):
        if len(self.waiting_list) > 0:
            blocked_proc = self.waiting_list[0]
            self.waiting_list.remove(blocked_proc)
            return blocked_proc
    
    
    ##################
    # main functions #
    ##################
    
    def unblock(self):
        unblk_proc = None
        if self.peek() != None and self.peek().amount <= self.available:
            unblk_proc = self.dequeue()
            unblk_proc.process.status = "ready"
            self.req(unblk_proc.process.pid, unblk_proc.amount)
            
        return unblk_proc
    
    def del_from_waiting_list(self, pid):
        for proc in self.waiting_list:
            if proc.pid == pid:
                self.waiting_list.remove(proc)
                return proc
        return None
    
    def req(self, pid, amount):
        if pid == "init":
            raise ModifyingInitProcessError
        elif amount > self.total:
            raise ValueError
        elif amount > self.available:
            raise BlockedError
            
        elif amount <= self.available:
            self.available -= amount
            self.consumed += amount
            if pid not in self.consumer_map:
                self.consumer_map[pid] = amount
            else:
                self.consumer_map[pid] += amount
            return amount
            
    def rel(self, amount):
        if self.consumed == 0 and amount >= 0:
            raise NonexistentObjectError
        elif amount > self.consumed or amount < 0:
            raise ValueError
        
        else:
            leftover = amount
            for pid in self.consumer_map:
                if leftover == 0:
                    break
                elif self.consumer_map[pid] <= leftover:
                    leftover -= self.consumer_map[pid]
                    self.consumer_map[pid] = 0
                else:
                    self.consumer_map[pid] -= leftover
                    
            self.consumed -= amount
            self.available += amount
        return amount
            
    def reset(self):
        self.available = self.total
        self.consumed = 0
        del self.waiting_list[:]
        self.consumer_map.clear()
        return
