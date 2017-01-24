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
        """ Returns the first element of self.waiting_list. """
        if len(self.waiting_list) > 0:
            return self.waiting_list[0]
        else:
            return None
            
    def dequeue(self):
        """ Returns the first element of self.waiting_list. """
        if len(self.waiting_list) > 0:
            blocked_proc = self.waiting_list[0]
            self.waiting_list.remove(blocked_proc)
            return blocked_proc
        return None
    
    ##################
    # main functions #
    ##################
    
    def unblock(self):
        """ Unblocks a process on self.waiting_list and attempts to acquire resources. """
        unblk_list = []
        unblk_proc = None
        while self.peek() != None and self.peek().amount <= self.available:
            unblk_proc = self.dequeue()
            unblk_proc.process.status = "ready"
            unblk_list.append(unblk_proc.process)
            self.req(unblk_proc.process.pid, unblk_proc.amount)
            
        return unblk_list
    
    def del_from_waiting_list(self, pid):
        """ Removes the given process from self.waiting_list. """
        for blk_proc in self.waiting_list:
            if blk_proc.process.pid == pid:
                self.waiting_list.remove(blk_proc)
                return blk_proc.process
        return None
    
    def req(self, pid, amount):
        """ Grants resources to the given process and catalogs the consumer in self.consumer_map. """
        if pid == "init":
            raise ModifyingInitProcessError
        elif amount > self.total or ( amount > self.available and pid in self.consumer_map ):
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
            
    def rel(self, pid, amount):
        """ Releases the resources held by the given process and catalogs the consumer in self.consumer_map. """
        if (self.consumed == 0 and amount >= 0) or pid not in self.consumer_map:
            raise NonexistentObjectError
        elif amount < 0 or (pid in self.consumer_map and amount > self.consumer_map[pid]):
            raise ValueError
        else:
            self.consumer_map[pid] -= amount
            
            if self.consumer_map[pid] == 0:
                del self.consumer_map[pid]
                
            self.consumed -= amount
            self.available += amount
        return amount
            
    def reset(self):
        """ Resets all data structures to the initial state. """
        self.available = self.total
        self.consumed = 0
        del self.waiting_list[:]
        self.consumer_map.clear()
        return
