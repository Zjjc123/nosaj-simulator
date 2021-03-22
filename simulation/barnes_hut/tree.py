from utils.constants import *
import operator

class Tree:
    def __init__(self, x, y, z, length, body=None):
        self.length = length
        self.x = x
        self.y = y
        self.z = z
        self.body = body # a Body object
        self.children = [] # will store more trees

        # NW, NE, SW, SE and Z from low to high

        self.tm = 0
        self.cm = (0, 0, 0)

    def insert_node(self, b):
        # find the child node which this body should go to
        # call function recursively
        #print(b.position)
        if len(self.children) > 1: # if the node already contains children
            #print('already has children')
            for i in len(self.children):
                if(self.children[i].contains(b)):
                    self.children[i].insert_node(self.children[i], b) # recursively insert child
                    break
        # expand quad tree
        # move current body into child node
        elif self.body != None: # if node contains particle but no children
            for i in range(2): # z
                new_z = i*self.length*0.5 + self.x
                for j in range(2): # y
                    new_y = j*self.length*0.5 + self.x
                    for k in range(2): # x
                        new_x = k*self.length*0.5 + self.x
                        new_tree = Tree(new_x, new_y, new_z, self.length/2, body=None) # create new tree
                        #print(new_x, new_y, new_z)
                        self.children.append(new_tree)
                        # find the appropriate node to put the child in
                        #print(new_tree.contains(self.body))
                        #print(type(b))
                        if(b != None):
                            if(new_tree.contains(b)):
                                # store child
                                new_tree.body = b
                                b = None
                                # remove reference
                        
                        if(self.body != None):
                            if(new_tree.contains(self.body)):
                                new_tree.body = self.body 
                                self.body = None
                        
                        computed_masses = new_tree.compute_mass()
                        new_tree.tm = computed_masses[0]
                        new_tree.cm = computed_masses[1]
        # if node is blank
        else:
            #print('nothing')
            self.body = b
        computed_masses = self.compute_mass()
        self.tm = computed_masses[0]
        self.cm = computed_masses[1]
    
    def contains(self, b):
        #print(type(b))
        #print(b.position)
        #print (b.position[0], " : ", self.x)
        if b.position[0] > self.x and b.position[0] <= self.x + self.length:
            #print(self.x, self.x + self.length)
            if b.position[1] > self.y and b.position[1] <= self.y + self.length:
                #print(self.y, self.y + self.length)
                if b.position[2] > self.z and b.position[2] <= self.z + self.length:
                    #print(self.z, self.z + self.length)
                    return True
        return False

    # returns 
    def compute_mass(self):
        if(self.body == None and len(self.children) == 0):
            self.tm = 0
            self.cm = (0,0,0)
            return (self.tm, self.cm)
        # if there is more than 1 child recursively into tree
        if len(self.children) > 1:
            nodes_queue = []
            for c in self.children:
                nodes_queue.append(c)

            while len(nodes_queue) > 0:
                first_node = nodes_queue.pop(0)
                mass_info = first_node.compute_mass()
                if(first_node.body != None):
                    self.tm += mass_info[0]
                    self.cm += tuple(mass_info[0] * i for i in first_node.body.position)
            
            self.cm  = self.cm/self.tm
            return(self.tm, self.cm)
        else:
            self.tm = self.body.mass
            self.cm = self.body.position
            return (self.tm, self.cm)