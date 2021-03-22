import numpy as np 
from simulation.body import Body
import matplotlib.pyplot as plt
from progress.bar import Bar

from simulation.init import *
from utils.constants import *
from simulation.barnes_hut.tree import Tree
import math

# ========== Functions ==========
def initialize(ic = InitialCondition.SIMPLE_TWO_BODY, args=None): 
    if ic == InitialCondition.SIMPLE_TWO_BODY:
        return simple_two_body()
    if ic == InitialCondition.SUN_EARTH_MOON:
        return sun_earth_moon()
    if ic == InitialCondition.SOLAR_SYSTEM:
        return solar_system()
    if ic == InitialCondition.RANDOM:
        return random(args['nrand'])


def update(nbodies, timestep):
    # creating tree

    base_tree = Tree(body=None, x=-0.5, y=-0.5, z=-0.5, length=2)
    for i in range(nbodies.shape[0]):
        #print(nbodies[i].position[0])
        base_tree.insert_node(nbodies[i])


    # force calculations 


    forces = np.zeros((nbodies.shape[0],3))
    energies = np.zeros(nbodies.shape[0])
    #print(nbodies[0].position)
    for i in range(nbodies.shape[0]): # for each body
        m1 = nbodies[i].mass
        p1 = nbodies[i].position
        #print(p1)
        
        queue = [] # breadth first search
        for c in base_tree.children: # append 8 children of base node
            if(c.body is not nbodies[i]):
                #if(c.body != None):
                    #print(c.body.position, p1)
                queue.append(c)
            #print(c.x)

        # something is at a distance of 0 but wtf is it idk i cry

        while(len(queue) > 0): # while something is in the queue
            new_node = queue.pop(0) # get next item
            #print(len(new_node.children) != 0)
            if(len(new_node.children) != 0 or new_node.body != None): # check if something exists in there
                p2 = new_node.cm # get 'location'
                dist = np.sqrt(np.sum((p1 - p2)**2)) # get distance from particle
                if(dist != 0):
                    if(len(new_node.children) == 0): # if there are no children
                        m2 = new_node.tm 
                        forces[i] += (p2 - p1) * G * m1 * m2 / (dist**3)
                        print(m2)
                        energies[i] +=  -G * m1 * m2 / dist
                    elif(new_node.length/dist > TREE_PRECISION): # if there ARE children, but the node is far enough
                        m2 = new_node.tm 
                        forces[i] += (p2 - p1) * G * m1 * m2 / (dist**3)
                        print(m2)
                        energies[i] +=  -G * m1 * m2 / dist
                    else: # if the node is too close/big, actually resolve it
                        for c in new_node.children:
                            if(c.body is not nbodies[i]):
                                if(c.body != None):
                                    print(c.body.position, p1)
                                queue.append(c)
            
        print(forces[i]) # one of them doesn't have a force on it
        nbodies[i].position += (nbodies[i].velocity * timestep) + (0.5 * forces[i] * timestep**2 / m1)
        nbodies[i].ke = 0.5 * m1 * np.sqrt(np.sum(nbodies[i].velocity ** 2))**2
        nbodies[i].velocity += forces[i] * timestep / m1
        nbodies[i].gpe = energies[i]
        
def run_nbody(nbodies, iterations, timestep):
    """
    0: x
    1: y
    2: z
    3: GPE
    4: KE
    """

    bar = Bar('Simulating', max=iterations)

    history = np.zeros((iterations,nbodies.shape[0],5)) 
    for i in range(iterations):
        update(nbodies, timestep)
        for j in range(nbodies.shape[0]):
            history[i, j, :3] = nbodies[j].position
            history[i, j, 3] = nbodies[j].gpe
            history[i, j, 4] = nbodies[j].ke
        bar.next()
    bar.finish()
    return history

def plot_history(history, iterations):
    cmaps = ['terrain','rainbow','ocean']
    skip=10
    for i in range(history.shape[1]):
        plt.scatter(history[:,i,0], history[:,i,1], s=1, c=np.arange(iterations),cmap=cmaps[i])
    plt.ylim(-5,5)
    plt.xlim(-5,5)
    plt.show()

def simulate(ts = 0.01, iterations = 1000, ic = InitialCondition.SIMPLE_TWO_BODY, args=None):
    global time_step
    time_step = ts
    global i
    i = iterations
    nbodies = initialize(ic, args)
    history = run_nbody(nbodies, i, time_step)
    # plot_history(history, i)
    print('Simulated!')
    return history, nbodies
    