import numpy as np 
from body import Body
import matplotlib.pyplot as plt
from constants import *

from enum import Enum

class InitialCondition(Enum):
    SIMPLE_TWO_BODY = 1
    SUN_EARTH_MOON = 2
    SOLAR_SYSTEM = 3
    RANDOM = 4

def simple_two_body():
    nbodies = np.empty(2,dtype=object)
    masses = np.array([10**11,10**11],dtype='float64')
    positions = np.array([[0,0,0],[1,1,0]],dtype='float64')
    velocities = np.array([[np.sqrt(masses[0]*G)/np.sqrt(4),0,0],[-np.sqrt(masses[0]*G)/np.sqrt(4),0,0]],dtype='float64')
    for i in range(2):
        nbodies[i] = Body(masses[i], positions[i], velocities[i])
    
    return nbodies

def sun_earth_moon():
    nbodies = np.empty(3,dtype=object)
    masses = np.array([SUN_MASS, EARTH_MASS, MOON_MASS],dtype='float64')
    velocities = np.array([[0,0,0], [0,EARTH_VELOCITY,0], [0,MOON_VELOCITY+EARTH_VELOCITY,0]],dtype='float64')
    positions = np.array([[0,0,0],[SUN_EARTH_DISTANCE,0,0],[EARTH_MOON_DISTANCE+SUN_EARTH_DISTANCE,0,0]],dtype='float64')
    for i in range(3):
        nbodies[i] = Body(masses[i], positions[i], velocities[i])
    
    return nbodies

def solar_system():
    print('stupid python')
    # nothing for now

def random(n, total_mass, z=False):
    mass = total_mass*np.ones((N,1))/N *10**10
    pos  = np.random.randn(N,3)
    vel  = np.random.randn(N,3)
        
    vel -= np.mean(mass * vel,0) / np.mean(mass)
    if z:
        nbodies = np.empty(n,dtype=object)
        for i in range(n):
            nbodies[i] = Body(mass[i], pos[i], vel[i])
        return nbodies
    else:
        pos[:,2] = 0
        vel[:,2] = 0
        nbodies = np.empty(n,dtype=object)
        for i in range(n):
            nbodies[i] = Body(mass[i], pos[i], vel[i])
        return nbodies