from Manager import *

if __name__ == "__main__":
    infile = "my_input2.txt"
    outfile = "57641580.txt"
    test_cases = "expected_output2.txt"
    m = Manager()
    m.run(infile, outfile)
    m.test(test_cases)