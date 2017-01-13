class BlockedError(Exception):
    pass

class ResourceControlBlock:
    def __init__(self, rid, total):
        self.rid = rid
        self.total = total
        self.available = total
        self.waiting_list = []
        self.consumer_map = dict()
        
    def req(self, amount):
        if amount > self.total:
            raise ValueError
            
        elif amount > self.available:
            raise BlockedError
            
        elif amount <= self.available:
            self.available -= amount
            return amount
            

            
        
    
        