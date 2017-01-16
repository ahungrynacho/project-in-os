class ProcessControlBlock:
    def __init__(self, pid, status, ready_list, pcb_parent, priority):
        self.pid = pid
        self.resource_map = dict() # map of currently consumed resources (rid : amount)
        self.status = status
        self.ready_list = ready_list
        self.pcb_parent = pcb_parent
        self.pcb_children = []
        self.priority = priority

class BlockedProcess:
    def __init__(self, pcb, rid, amount):
        self.process = pcb
        self.rid = rid
        self.amount = amount
        
class Resource:
    def __init__(self, rid, amount):
        self.rid = rid
        self.amount = amount
        
    