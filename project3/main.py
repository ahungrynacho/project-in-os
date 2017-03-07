from manager import Manager

def main():
    m = Manager()
    
    # m.run(False, "input1.txt", "input2.txt", "57641580.txt")
    # m.reset()
    # m.run(True, "input1.txt", "input2.txt", "576415802.txt")
    
    virt_addr_init = [
        "my_init0.txt", 
        "my_init1.txt", 
        "my_init2.txt", 
        "my_init3.txt"
        ]
        
    virt_addr_input = [
        "my_input0.txt", 
        "my_input1.txt", 
        "my_input2.txt", 
        "my_input3.txt"
        ]
    exp_output = [
        "my_output0.txt", 
        "my_output1.txt", 
        "my_output2.txt", 
        "my_output3.txt"
        ]
    exp_output_TLB = [
        "my_output_TLB0.txt", 
        "my_output_TLB1.txt", 
        "my_output_TLB2.txt", 
        "my_output_TLB3.txt"
        ]
    authors = [
        "Professor Bic", 
        "Brian Luu", 
        "Brian Huynh", 
        "Brian Luu"
        ]
    output = "my_57641580"
    output_TLB = "my_57641580_TLB"
    ext = "txt"

    # m.run(False, virt_addr_init[2], virt_addr_input[2], m.parse_filename(output, 2, ext))
    for i in range(0, len(virt_addr_init), 1):
        if i == 0 or i == 1 or i == 2:
            continue
        
        m.run(False, virt_addr_init[i], virt_addr_input[i], m.parse_filename(output, i, ext))
        m.test(authors[i], exp_output[i], False)
        m.reset()
        
        m.run(True, virt_addr_init[i], virt_addr_input[i], m.parse_filename(output_TLB, i, ext))
        m.test(authors[i], exp_output_TLB[i], True)
        m.reset()
    

if __name__ == "__main__":
    main()