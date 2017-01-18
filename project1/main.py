from manager import Manager

if __name__ == "__main__":
    manager = Manager("input.txt")
    
    """
    Test Cases
    
    Deleting a parent process will delete its children.
    init x x x x z z x z x x init
    
    Deleting a blocked process will remove itself from the blocked list and all waiting lists and free resources.
    init x x x x p p q q r r x p q r x x x p x error
    
    Releasing more than the total available resources.
    init error
    
    Releasing a resource that hasn't been requested.
    init error
    
    Releasing a resource that doesn't exist.
    init error
    
    Deleting a process that doesn't exist.
    init error
    
    Creating a duplicate process.
    init x error
    
    Creating a process with priority 0.
    init error
    
    Deleting init.
    init error
    
    Init acquiring a resource.
    init error
    
    Init releasing a resource.
    init error
    
    Requesting 0 resources.
    init x x x
    
    Releasing all resources and destroying all processes.
    init x x x x x y y z z init
    """
    print manager.run()
    
    print manager.list_resources()
    print manager.list_processes(manager.ready_list)
    print manager.list_processes(manager.blocked_list)