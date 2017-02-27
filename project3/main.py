from manager import Manager

def main():
    m = Manager()
    m.run("VA_init.txt", "VA_input.txt", "57641580.txt")
    # m.test("expected_output.txt")

if __name__ == "__main__":
    main()