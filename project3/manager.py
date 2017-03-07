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
    TLB_SIZE = 4        # number of entries in the TLB
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
            mem.append(0)
        return mem
        
    def __init__(self):
        self.phys_mem = self.init_phys_mem(Manager.PM_SIZE)
        self.bitmap = BitMap(Manager.BM_SIZE)
        self.TLB = TLB(Manager.TLB_SIZE)
        
        self.seg_table = []     # elements are SegmentTableEntry()
        self.page_table = []        # elements are PageTableEntry()
        self.VA_input = []      # elements are VirtualAddress()
        
        self.expected_output = []       # elements are string
        self.generated_output = []      # elements are string

    def output_phys_mem(self):
        """ (index, value) """ 
        for i in range(0, Manager.PM_SIZE, 1):
            if self.phys_mem[i] != 0:
                print(i, self.phys_mem[i])
                
    def output_seg_table(self):
        print("segment table")
        print("(index, page table address)")
        for i in range(0, Manager.FRAME_SIZE, 1):
            if self.phys_mem[i]:
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
        """ 
        Reads from the physical address 
        translated from the virtual address
        with or without the TLB. 
        """
        sp = self.sp_mask(virt_addr)
        s = self.s_mask(virt_addr)
        p = self.p_mask(virt_addr)
        w = self.w_mask(virt_addr)
        
        if TLB and self.TLB.contains_entry(sp):     # TLB hit
            frame_addr = self.TLB.get_addr(sp)      # PM[PM[s] + p]
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
                return str(frame_addr + w)
            
    def write_virt_mem(self, virt_addr, TLB):
        """ 
        Writes to the physical address
        translated from the virtual address
        with or without the TLB.
        """
        sp = self.sp_mask(virt_addr)
        s = self.s_mask(virt_addr)
        p = self.p_mask(virt_addr)
        w = self.w_mask(virt_addr)

        if TLB and self.TLB.contains_entry(sp):     # TLB hit
            frame_addr = self.TLB.get_addr(sp)
            if frame_addr == -1:
                return "h pf"
            else:
                self.TLB.update(frame_addr)
                return "h " + str(frame_addr + w)
        
        elif TLB:       # TLB miss
            frame_addr = self.phys_mem[self.phys_mem[s] + p]
            if self.phys_mem[s] == 0:       # non-existent page table
                self.phys_mem[s] = self.bitmap.malloc(Manager.PAGE_TABLE) * Manager.FRAME_SIZE
                data_page_addr = self.bitmap.malloc(Manager.DATA_PAGE) * Manager.FRAME_SIZE
                self.phys_mem[self.phys_mem[s] + p] = data_page_addr
                self.TLB.insert(TLB_Entry(sp, data_page_addr))
                return "m " + str(data_page_addr + w)
                
            elif self.phys_mem[s] == -1 or frame_addr == -1:
                return "m pf"
                
            elif frame_addr == 0:       # non-existent data page within page table
                data_page_addr = self.bitmap.malloc(Manager.DATA_PAGE) * Manager.FRAME_SIZE
                self.phys_mem[self.phys_mem[s] + p] = data_page_addr
                self.TLB.insert(TLB_Entry(sp, data_page_addr))     # insert new blank frame address into TLB
                return "m " + str(data_page_addr + w)
                
            else:
                self.TLB.insert(TLB_Entry(sp, frame_addr))
                return "m " + str(frame_addr + w)           
            
        else:       # no TLB
            frame_addr = self.phys_mem[self.phys_mem[s] + p]
            if self.phys_mem[s] == 0:       # non-existent page table
                self.phys_mem[s] = self.bitmap.malloc(Manager.PAGE_TABLE) * Manager.FRAME_SIZE
                data_page_addr = self.bitmap.malloc(Manager.DATA_PAGE) * Manager.FRAME_SIZE
                self.phys_mem[self.phys_mem[s] + p] = data_page_addr
                return str(data_page_addr + w)
                
            elif self.phys_mem[s] == -1 or frame_addr == -1:
                return "pf"
                
            elif frame_addr == 0:       # non-existent data page within page table
                data_page_addr = self.bitmap.malloc(Manager.DATA_PAGE) * Manager.FRAME_SIZE
                self.phys_mem[self.phys_mem[s] + p] = data_page_addr
                return str(data_page_addr + w)
                
            else:
                return str(frame_addr + w)
          

    def exec_virt_mem(self, TLB):
        """ Executes read/write operations for each virtual address. """
        buf = []
        output = None
        for entry in self.VA_input:
            if entry.op:
                output = self.write_virt_mem(entry.virt_addr, TLB)
            else:
                output = self.read_virt_mem(entry.virt_addr, TLB)
            
            if output != None:
                buf.append(output)
                
        return buf
    
    ##########
    # PUBLIC #
    ##########
    
    def run(self, TLB, VA_init_file, VA_input_file, outfile):
        """ 
        Parses input files into lists. 
        Initializes and executes the virtual memory.
        Writes the generated output to a file.
        """
        init_list = self.read_input(VA_init_file)       # 2D list where each sublist is a line in the file
        for i in range(0, len(init_list[0]), 2):      # parse virtual address initialization file
            self.seg_table.append(SegmentTableEntry(
                                                int(init_list[0][i]), 
                                                int(init_list[0][i+1])
                                                ))        # assign element in segment table

        for i in range(0, len(init_list[1]), 3):
            self.page_table.append(PageTableEntry(
                                                int(init_list[1][i]), 
                                                int(init_list[1][i+1]), 
                                                int(init_list[1][i+2])
                                                ))
        
        VA_input_list = self.read_input(VA_input_file)[0]       # parse virtual address input file
        for i in range(0, len(VA_input_list), 2):
            self.VA_input.append(VirtualAddress(
                                                int(VA_input_list[i]), 
                                                int(VA_input_list[i+1])
                                                ))
            
        self.init_virt_mem()
        self.generated_output = self.exec_virt_mem(TLB)
        self.write_output(outfile, " ".join(self.generated_output))
        
        # self.bitmap.output_bitmap()
        # self.output_seg_table()
        
        return
    
    def reset(self):
        self.phys_mem = self.init_phys_mem(Manager.PM_SIZE)
        self.bitmap.reset()
        self.TLB.reset()
        del self.seg_table[:]
        del self.page_table[:]
        del self.VA_input[:]
        del self.generated_output[:]
        del self.expected_output[:]
        
    def parse_filename(self, name, test_num, ext):
        return "{}_{}.{}".format(name, test_num, ext)
    
    def test(self, author, expected_output, TLB):
        temp = self.read_input(expected_output)[0]
        print("---------------------------------------")
        print("*** " + author + " ***")
        if TLB:
            print("*** TLB ON ***")
            for i in range(0, len(temp), 2):
                self.expected_output.append(str(temp[i] + " " + temp[i+1]))
                
        else:
            print("*** TLB OFF ***")
            for e in temp:
                self.expected_output.append(e)
        
        for i in range(0, len(self.expected_output), 1):
            if self.expected_output[i] != self.generated_output[i]:
                print("FAIL : expected {}, generated {}".format(self.expected_output[i], self.generated_output[i]))
            else:
                print("PASS")
        print("---------------------------------------\n")
    