class BlockedError(Exception):
    pass

class ResourceControlBlock:
    def __init__(self, rid, total):
        self.rid = rid
        self.total = total
        self.available = total
        self.consumed = 0
        self.waiting_list = [] # elements are BlockedProcess()
        self.consumer_map = dict() # (pid : amount)
        
    def req(self, amount):
        if amount > self.total:
            raise ValueError
            
        elif amount > self.available:
            raise BlockedError
            
        elif amount <= self.available:
            self.available -= amount
            self.consumed += amount
            return amount
            
    def rel(self, amount):
        if amount > self.consumed or amount < 0:
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
                    
            self.available += amount
        
        return
            
    def reset(self):
        self.available = self.total
        self.consumed = 0
        del self.waiting_list[:]
        self.consumer_map.clear()
        return

            
            
    

            
        
    
        