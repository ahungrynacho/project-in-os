from tables import SegmentTableEntry
from tables import PageTableEntry
from tables import VirtualAddress
from bitmap import BitMap
from TLB import TLB
from TLB import TLB_Entry

class Manager(object):
    PM_SIZE = 524288        # BM_SIZE * FRAME_SIZE
    BM_SIZE = 1024      # number of frames (2 ** 10)
    FRAME_SIZE = 512        # (2 ** 9)
    SEG_TABLE = DATA_PAGE = 1       # macro for number of frames needed
    PAGE_TABLE = 2      # macro for number of frames needed
    MASK9 = 511     # 9 LSB mask
    MASK10 = 1023       # 10 LSB mask
    
    ###########
    # PRIVATE #
    ###########
    
    def init_phys_mem(self, length):
        mem = []
        for i in range(0, length, 1):
            if i < 512:
                mem.append(0)
            else:
                mem.append(-1)
        return mem
        
    def __init__(self):
        self.phys_mem = [0 for i in range(0, Manager.PM_SIZE, 1)]
        self.bitmap = BitMap(Manager.BM_SIZE)
        self.TLB = TLB(4)
        
        self.seg_table = []     # elements are SegmentTableEntry()
        self.page_table = []        # elements are PageTableEntry()
        self.VA_input = []      # elements are VirtualAddress()
        
        self.expected_output = []       # elements are string
        self.generated_output = []      # elements are string

    def init_virt_mem(self):
        """ 
        Initializes virtual memory by reading 
        segment and page table entries into
        physical memory while updating the bitmap. 
        """
        for entry in self.seg_table:
            self.phys_mem[entry.seg_index] = entry.PT_addr
            self.bitmap.malloc_addr(Manager.PAGE_TABLE, entry.PT_addr)
            
        for entry in self.page_table:
            self.phys_mem[self.phys_mem[entry.seg_index] + entry.page_index] = entry.DP_addr
            self.bitmap.malloc_addr(Manager.DATA_PAGE, entry.DP_addr)
        
        return
    
    def sp_mask(self, virt_addr):
        """ Returns concatenated segment and page table index. """
        return virt_addr >> 9
        
    def s_mask(self, virt_addr):
        """ Returns segment table index. """
        return (virt_addr >> 19) & Manager.MASK9
        
    def p_mask(self, virt_addr):
        """ Returns page table index. """
        return (virt_addr >> 9) & Manager.MASK10
        
    def w_mask(self, virt_addr):
        """ Returns data page index. """
        return virt_addr & Manager.MASK9
        
    def read_virt_mem(self, virt_addr, TLB):
        sp = self.sp_mask(virt_addr)
        s = self.s_mask(virt_addr)
        p = self.p_mask(virt_addr)
        w = self.w_mask(virt_addr)
        
        if TLB and self.TLB.contains_entry(sp):     # TLB hit
            frame_addr = self.TLB.get_addr(sp)
            if frame_addr == -1:
                return "h pf"
            elif frame_addr == 0:
                return "h err"
            else:
                self.TLB.update(frame_addr)
                return "h " + str(frame_addr + w)
                
        elif TLB:       # TLB miss
            frame_addr = self.phys_mem[self.phys_mem[s] + p]
            if self.phys_mem[s] == -1 or frame_addr == -1:
                return "m pf"
            elif self.phys_mem[s] == 0 or frame_addr == 0:
                return "m err"
            else:
                self.TLB.insert(TLB_Entry(sp, frame_addr))
                return "m " + str(frame_addr + w)
                
        else:       # no TLB
            frame_addr = self.phys_mem[self.phys_mem[s] + p]
            if self.phys_mem[s] == -1 or frame_addr == -1:
                return "pf"
            elif self.phys_mem[s] == 0 or frame_addr == 0:
                return "err"
            else:
                self.TLB.insert(TLB_Entry(sp, frame_addr))
                return frame_addr + w
            
    def write_virt_mem(self, virt_addr, TLB):
        sp = self.sp_mask(virt_addr)
        s = self.s_mask(virt_addr)
        p = self.p_mask(virt_addr)
        w = self.w_mask(virt_addr)

        if self.phys_mem[s] == 0:       # independent of TLB
            start = self.bitmap.malloc(Manager.PAGE_TABLE)
            for i in range(start, start + (Manager.PAGE_TABLE * Manager.FRAME_SIZE), 1):
                self.phys_mem[i] = 0
            return None
        
        if TLB and self.TLB.contains_entry(sp):     # TLB hit
            frame_addr = self.TLB.get_addr(sp)
            if self.phys_mem[s] == -1 or frame_addr == -1:
                return "h pf"
            else:
                self.TLB.update(frame_addr)
                return "h " + str(frame_addr + w)
        
        elif TLB:       # TLB miss
            frame_addr = self.phys_mem[self.phys_mem[s] + p]
            if self.phys_mem[s] == -1 or frame_addr == -1:
                return "m pf"
            elif frame_addr == 0:
                start = self.bitmap.malloc(Manager.DATA_PAGE)
                self.TLB.insert(TLB_Entry(sp, start))     # insert new blank frame address into TLB?
                for i in range(start, start + (Manager.DATA_PAGE * Manager.FRAME_SIZE), 1):
                    self.phys_mem[i] = 0
                return None
            else:
                self.TLB.insert(TLB_Entry(sp, frame_addr))
                return "m " + str(frame_addr + w)           
            
        else:       # no TLB
            frame_addr = self.phys_mem[self.phys_mem[s] + p]
            if self.phys_mem[s] == -1 or frame_addr == -1:
                return "pf"  
            elif frame_addr == 0:
                start = self.bitmap.malloc(Manager.DATA_PAGE)
                for i in range(start, start + (Manager.DATA_PAGE * Manager.FRAME_SIZE), 1):
                    self.phys_mem[i] = 0
                return None
            else:
                return frame_addr + w
          

    def exec_virt_mem(self, TLB):
        result = ""
        addr = None
        for entry in self.VA_input:
            if entry.op:
                addr = self.write_virt_mem(entry.virt_addr, TLB)
            else:
                addr = self.read_virt_mem(entry.virt_addr, TLB)
            
            if addr != None:
                result += str(addr) + " "
            
        print(result)
        return
            
    def output_phys_mem(self):
        """ (index, value) """ 
        for i in range(0, Manager.PM_SIZE, 1):
            if self.phys_mem[i] != -1:
                print(i, self.phys_mem[i])
                
    def read_input(self, file):
        infile = open(file, 'r')
        buf = []
        for line in infile:
            buf.append(line.strip('\n').split())
        infile.close()
        return buf
        
    def write_output(self, file, message):
        outfile = open(file, 'w')
        outfile.write(message)
        outfile.close()
        return
    
    ##########
    # PUBLIC #
    ##########
    
    def run(self, TLB, VA_init_file, VA_input_file, outfile):
        """ 
        Parses input files into lists. 
        Initializes and executes the virtual memory.
        Writes the generated output to a file.
        """
        for line in self.read_input(VA_init_file):
            if len(line) == 2:      # assign element in segment table
                self.seg_table.append(SegmentTableEntry(int(line[0]), int(line[1])))
            else:
                for i in range(0, len(line), 3):
                    self.page_table.append(PageTableEntry(int(line[i]), int(line[i+1]), int(line[i+2])))
        
        VA_input_list = self.read_input(VA_input_file)[0]
        for i in range(0, len(VA_input_list), 2):
            self.VA_input.append(VirtualAddress(int(VA_input_list[i]), int(VA_input_list[i+1])))
            
        self.init_virt_mem()
        self.exec_virt_mem(TLB)
        # self.output_phys_mem()
        # self.bitmap.output_bitmap()
        
        self.write_output(outfile, " ".join(self.generated_output))   
        
        return
    
    def test(self, expected_output):
        for e in self.read_input(expected_output)[0]:
            self.expected_output.append(e)
            
        for i in range(0, len(self.expected_output), 1):
            if self.expected_output[i] != self.generated_output[i]:
                print("FAIL : expected {}, generated {}".format(self.expected_output[i], self.generated_output[i]))
            else:
                print("PASS")
    