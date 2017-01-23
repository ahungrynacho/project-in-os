from manager import Manager

if __name__ == "__main__":
    manager = Manager("", None)
    manager.run()
    print manager.test()
    
    print "--- TEST COMPLETE ---"
    print manager.list_resources()
    print manager.list_processes(manager.ready_list)
    print manager.list_processes(manager.blocked_list)





























