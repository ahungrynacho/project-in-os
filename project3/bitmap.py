class BitMap(object):
    def __init__(self, length):
        self.length = length
        self.bitmap = [0 for i in range(0, length, 1)]
        self.bitmap[0] = 1      # segment table always allocated to the first frame
        
    def output_bitmap(self):
        """ (index, value) """
        for i in range(0, self.length, 1):
            if self.bitmap[i]:
                print(i, self.bitmap[i])
                
    def malloc_addr(self, frames, addr):
        """ 
        Updates the bitmap for non-negative addresses 
        indicating allocated frames and then returns the frame's index.
        """
        if addr < 0:
            return None
            
        index = addr / 512
        if frames == 1:
            self.bitmap[index] = 1
        elif frames == 2:
            self.bitmap[index] = 1
            self.bitmap[index+1] = 1
            
        return index
    
    def malloc(self, frames):
        """ 
        Searches for free frames, updates the bitmap to indicate allocated
        frames, and then returns the frame's index.
        """
        if frames == 1:
            for i in range(0, self.length, 1):
                if self.bitmap[i] == 0:
                    self.bitmap[i] = 1
                    return i
                
        elif frames == 2:
            for i in range(0, self.length-1, 1):
                if self.bitmap[i] == 0 and self.bitmap[i+1] == 0:
                    self.bitmap[i] = 1
                    self.bitmap[i+1] = 1
                    return i
                    
        return None