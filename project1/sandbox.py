class Node:
    def __init__(self, value, parent):
        self.parent = parent
        self.value = value
        self.children = []
        self.leaf = True
        
    def add_children(self, child):
        child.parent = self
        self.children.append(child)
        self.leaf = False
        return
    
    def list_children(self):
        result = ""
        for child in self.children:
            result += "{} ".format(str(child.value))
        return result
        
    def delete_subtree(self, root):
        """ Deletes all children of the root including the root. """
        if root == None:
            return
            
        del self.children[:]
        # print root.value
        # if root.parent != None and root.leaf:
        #     return
        # else:
        #     for child in root.children:
        #         self.delete_subtree(child)

        return

def remove_from_list(array, element):
    array = []
    array.append(100)
    return

def repoint(obj):
    del obj
    return
if __name__ == "__main__":
    
    # array = [5, 10, 15]
    # remove_from_list(array, 10)
    # print array
    
    root = Node(0, None)
    # print "outside function " + str(id(root))
    for i in range(1, 4, 1):
        root.add_children(Node(i, root))
        
    for i in range(4, 7, 1):
        parent = root.children[0]
        parent.add_children(Node(i, parent))
        
    # print root.list_children()
    root.delete_subtree(root)
    
    empty = []
    for x in empty:
        print x
    # print root.list_children()
    
    
    # print repoint(root)
    # root.delete()
    # print root
    # root.delete_tree(root)
    # print root.list_children()