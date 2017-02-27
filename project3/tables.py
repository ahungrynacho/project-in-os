class SegmentTableEntry(object):
    def __init__(self, seg_index, PT_addr):
        self.seg_index = seg_index
        self.PT_addr = PT_addr      # Page Table address
        
    def __str__(self):
        return "({}, {})".format(self.seg_index, self.PT_addr)

class PageTableEntry(object):
    def __init__(self, page_index, seg_index, DP_addr):
        self.page_index = page_index
        self.seg_index = seg_index
        self.DP_addr = DP_addr      # Data Page address
    
    def __str__(self):
        return "({}, {}, {})".format(self.page_index, self.seg_index, self.DP_addr)
        
class VirtualAddress(object):
    def __init__(self, op, virt_addr):
        self.op = op        # operation
        self.virt_addr = virt_addr
        
    def __str__(self):
        return "({}, {})".format(self.op, self.virt_addr)