class BitMap(object):
    
    def init_bitmap(self, length):
        bitmap = []
        for i in range(0, length, 1):
            bitmap.append(0)
        bitmap[0] = 1       # segment table always allocated to the first frame
        return bitmap
        
    def __init__(self, length):
        self.length = length
        self.bitmap = self.init_bitmap(length)
        
    def reset(self):
        self.bitmap = self.init_bitmap(self.length)
        
    def output_bitmap(self):
        print("bitmap")
        print("(index, physical address, value)")
        for i in range(0, self.length, 1):
            if self.bitmap[i]:
                print(i, i * 512, self.bitmap[i])
                
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