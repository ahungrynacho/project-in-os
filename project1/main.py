from manager import Manager

if __name__ == "__main__":
    manager = Manager("input.txt")
    # init x x x x z z x z x x init
    # init x x x x p p q q r r x p q r x x x p x error
    print manager.run()
    
    print manager.list_resources()
    print manager.list_processes(manager.ready_list)
    print manager.list_processes(manager.blocked_list)