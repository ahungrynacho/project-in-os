class TLB_Entry(object):
    MAX_INDEX = 3
    def __init__(self, sp, frame_addr):
        self.sp = sp
        self.frame_addr = frame_addr
        self.rank = TLB_Entry.MAX_INDEX

class TLB(object):
    
    ###########
    # PRIVATE #
    ###########
    
    def __init__(self, length):
        self.length = length
        self.TLB = []       # elements are TLB_Entry()
       
    def decrement(self):
        for entry in self.TLB:
            entry.rank -= 1
        return
    
    def remove(self):
        for entry in self.TLB:
            if entry.rank < 0:
                self.TLB.remove(entry)
        return
    
    ##########
    # PUBLIC #
    ##########

    def reset(self):
        del self.TLB[:]
        
    def update(self, frame_addr):
        """ 
        Updates the LRU ranks of entries in 
        the TLB when there is a TLB hit. 
        """
        entry = None
        for e in self.TLB:
            if e.frame_addr == frame_addr:
                entry = e
                break
        
        for e in self.TLB:
            if e.rank > entry.rank:
                e.rank -= 1
        entry.rank = TLB_Entry.MAX_INDEX
        return
        
    def insert(self, entry):
        """ 
        Inserts a new entry into the 
        TLB and deletes the LRU entry. 
        """
        self.decrement()
        self.TLB.append(entry)
        self.remove()
    
    def contains_entry(self, sp):
        """ 
        Returns True if an entry with the concatenated 
        segment and page table index (sp) exists in the TLB.
        """
        for entry in self.TLB:
            if entry.sp == sp:
                return True
        return False
    
    def get_addr(self, sp):
        """ Returns PM[PM[s] + p] """
        for entry in self.TLB:
            if entry.sp == sp:
                return entry.frame_addr
        return None
        
        
    