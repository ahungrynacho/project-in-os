from manager import Manager

def main():
    m = Manager()
    
    virt_addr_init = ["init0.txt", "init1.txt", "init2.txt"]
    virt_addr_input = ["input0.txt", "input1.txt", "input2.txt"]
    exp_output = ["output0.txt", "output1.txt", "output2.txt"]
    exp_output_TLB = ["output_TLB0.txt", "output_TLB1.txt", "output_TLB2.txt"]
    authors = ["Professor Bic", "Brian Luu", "Brian Huynh"]
    output = "57641580"
    output_TLB = "57641580_TLB"
    ext = "txt"

    # m.run(False, virt_addr_init[2], virt_addr_input[2], m.parse_filename(output, 2, ext))
    for i in range(0, len(virt_addr_init), 1):
        if i == 1:
            continue
        
        m.run(False, virt_addr_init[i], virt_addr_input[i], m.parse_filename(output, i, ext))
        m.test(authors[i], exp_output[i], False)
        m.reset()
        
        m.run(True, virt_addr_init[i], virt_addr_input[i], m.parse_filename(output_TLB, i, ext))
        m.test(authors[i], exp_output_TLB[i], True)
        m.reset()
    

if __name__ == "__main__":
    main()