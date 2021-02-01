import numpy as np 
from body import Body
import matplotlib.pyplot as plt
from constants import *

from enum import Enum

class InitialCondition(Enum):
    SIMPLE_TWO_BODY = 1

def simple_two_body():
    nbodies = np.empty(2,dtype=object)
    masses = np.array([10**11,10**11],dtype='float64')
    positions = np.array([[0,0,0],[1,1,0]],dtype='float64')
    velocities = np.array([[np.sqrt(masses[0]*G)/np.sqrt(4),0,0],[-np.sqrt(masses[0]*G)/np.sqrt(4),0,0]],dtype='float64')
    for i in range(2):
        nbodies[i] = Body(masses[i], positions[i], velocities[i])
    
    return nbodies