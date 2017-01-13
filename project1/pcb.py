class ProcessControlBlock:
    def __init__(self, pid, resources, status, ready_list, pcb_parent, priority):
        self.pid = pid
        self.resources = resources,
        self.status = status
        self.ready_list = ready_list
        self.pcb_parent = pcb_parent
        self.pcb_children = []
        self.priority = priority
        
        
    