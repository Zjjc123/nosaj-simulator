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

def simple_two_body(render = False):
    # timestep of 0.00001
    if not render:
        nbodies = np.empty(2,dtype=object)
        masses = np.array([10**11,10**11],dtype='float64')
        positions = np.array([[0,0,0],[1,1,0]],dtype='float64')
        velocities = np.array([[np.sqrt(masses[0]*G)/np.sqrt(4),0,0],[-np.sqrt(masses[0]*G)/np.sqrt(4),0,0]],dtype='float64')
        for i in range(2):
            nbodies[i] = Body(masses[i], positions[i], velocities[i])
            
        return nbodies
    else:
        return {'timestep':0.0001, 'multiplier': 200, 'sizes':[10,10]}

def sun_earth_moon(render = False):
    #timestep of 100 or 1000
    if not render:
        nbodies = np.empty(3,dtype=object)
        masses = np.array([SUN_MASS, EARTH_MASS, MOON_MASS],dtype='float64') # SUN, EARTH, MOON
        velocities = np.array([[0,0,0], [0,EARTH_VELOCITY,0], [0,MOON_VELOCITY+EARTH_VELOCITY,0]],dtype='float64')
        positions = np.array([[0,0,0],[SUN_EARTH_DISTANCE,0,0],[EARTH_MOON_DISTANCE+SUN_EARTH_DISTANCE,0,0]],dtype='float64')
        for i in range(3):
            nbodies[i] = Body(masses[i], positions[i], velocities[i])

        return nbodies
    else:
       return {'timestep':1000, 'multiplier': 1000, 'sizes':[30, 10, 4]} 

def solar_system(render = False):
    masses = np.array([SUN_MASS, MERCURY_MASS, VENUS_MASS, EARTH_MASS, MARS_MASS, JUPITER_MASS, SATURN_MASS, URANUS_MASS, NEPTUNE_MASS],dtype='float64')
    if not render:
        nbodies = np.empty(9,dtype=object)
        velocities = np.array([[0,0,0], [0,MERCURY_VELOCITY,0], [0,VENUS_VELOCITY,0],[0,EARTH_VELOCITY,0], [0,MARS_VELOCITY,0], [0,JUPITER_VELOCITY,0], [0,SATURN_VELOCITY,0], [0,URANUS_VELOCITY,0], [0,NEPTUNE_VELOCITY,0]],dtype='float64')
        positions = np.array([[0,0,0],[SUN_MERCURY_DISTANCE,0,0],[SUN_VENUS_DISTANCE,0,0],[SUN_EARTH_DISTANCE,0,0],[SUN_MARS_DISTANCE,0,0],[SUN_JUPITER_DISTANCE,0,0],[SUN_SATURN_DISTANCE,0,0],[SUN_URANUS_DISTANCE,0,0],[SUN_NEPTUNE_DISTANCE,0,0]],dtype='float64')
        for i in range(9):
            nbodies[i] = Body(masses[i], positions[i], velocities[i])
    
        return nbodies
    else:
        sizes = []
        for i in range(9):
            if i==0:
                sizes.append(12)
            else:
                sizes.append(np.max([5, 8*np.log10(masses[i])/np.log10(masses[0])]))
        return {'timestep':1000, multiplier: 1000, 'sizes':sizes} 

def random(n=2, render = False, z=False):
    if not render:
        mass = np.ones((n,1))  *10**11
        pos  = np.random.randn(n,3)
        vel  = np.random.randn(n,3)*10
            
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
    else:
        sizes = []
        for i in range(n):
            sizes.append(10)
        return {'timestep':0.00001, 'multiplier': 200, 'sizes':sizes}