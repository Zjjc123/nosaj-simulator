import pyglet
import numpy as np
from pyglet import shapes
from init import *
from constants import *

import simulator

# render scale
rendering_multplier = 200
# window size
rendering_size = [1280, 720]
rendering_offset = [rendering_size[0]/2, rendering_size[1]/2]

# timestep skipping
skip = 100
trail_length = 40

# screenshot
ss = False

# graph y-offset
graphing_offset = 200

red = (231, 76, 60)
green = (0, 255, 0)
green_light = (0, 150, 0)
blue = (52, 152, 219)
white = (255, 255, 255)
fontsize = 20

# render batches
particle_batch = pyglet.graphics.Batch()
n_batch = pyglet.graphics.Batch()
graph_batch = pyglet.graphics.Batch()
text_batch = pyglet.graphics.Batch()

# array storing bodies, trails, and energy graphics
bodies = []
trail = []
energy = []

# use simulate.py to run nbody
history = simulator.simulate(0.0001, 100000, ic = InitialCondition.SIMPLE_TWO_BODY, N=2)

# creating window
window = pyglet.window.Window(width=rendering_size[0], height=rendering_size[1])

# normalize energy by total energy (min-max normalization)
total_energy = history[:,:,3] + history[:,:,4]
history[:,:,3] = history[:,:,3]/(np.max(total_energy)-np.min(total_energy))
history[:,:,4] = history[:,:,4]/(np.max(total_energy)-np.min(total_energy))

# set count, which tracks the number of timesteps rendered
count = 0

# generate objects for each body
for i in range(history.shape[1]):
    # instantiate new n body circle
    newbody = shapes.Circle(history[0,i,0] * rendering_multplier+rendering_offset[0],
                            history[0,i,1] * rendering_multplier+rendering_offset[1],
                            10, color=green, batch=n_batch)
    bodies.append(newbody)

# instantiate trail
for i in range(len(bodies)):
        # for each particle in the trail length:
        for j in range(trail_length):
            # instantiate trail object
            newbody = shapes.Circle(history[0,i,0] * rendering_multplier+rendering_offset[0],
                                    history[0,i,1] * rendering_multplier+rendering_offset[1],
                                    float(max(4, 10*((trail_length) - j)/((trail_length))) - 2),  # Jay Pog's big brained formula to normalize size from 4 - 10
                                    color=green_light, 
                                    batch=particle_batch)
            trail.append(newbody)

# instantiate labels
label_ke = pyglet.text.Label('Total Kinetic Energy = %.2f' % 0, font_size = fontsize, x= rendering_size[0]/50, y=graphing_offset*0.1+fontsize*2, color=red + (255,), batch=text_batch, anchor_x='left')
label_gpe = pyglet.text.Label('Total Gravitational Potential Energy = %.2f' % 0, font_size = fontsize, x= rendering_size[0]/50, y=graphing_offset*0.1+fontsize, color=blue + (255,), batch=text_batch, anchor_x='left')
label_sum = pyglet.text.Label('Total Energy = %.2f' % 0, font_size = fontsize, x= rendering_size[0]/50, y=graphing_offset*0.1, color=white + (255,), batch=text_batch, anchor_x='left')

# drawing function
@window.event
def on_draw():
    # clear window
    window.clear()

    # render batches
    particle_batch.draw()
    n_batch.draw()
    graph_batch.draw()
    text_batch.draw()

# update function
def update(dt, skip):
    global count # python global variables

    # N BODIES
    # for each body:
    for i in range(len(bodies)):
        # update position of body objects
        bodies[i].position = (history[count,i,0]*rendering_multplier+rendering_offset[0], 
                                history[count,i,1] * rendering_multplier+rendering_offset[1])
    
    # python global variables. make a list to hold new objects
    global trail
    particles = min((skip*trail_length), count+1) # trail length
    
    # PARTICLES
    # for each body:
    for i in range(len(bodies)):
        # for each particle in the trail length:
        for j in range(trail_length):
            if skip*j < count:
                # instantiate trail object
                trail[j+i*trail_length].position = (history[count-(j*skip),i,0] * rendering_multplier+rendering_offset[0],
                                        history[count-(j*skip),i,1] * rendering_multplier+rendering_offset[1])
            else:
                trail[j+i*trail_length].position = (history[count,i,0]*rendering_multplier+rendering_offset[0], 
                            history[count,i,1] * rendering_multplier+rendering_offset[1])

    global energy
    
    # GRAPH
    # for each past timestep:
    current_kesum = 0
    current_gpesum = 0
  
    # add up gpe and ke
    for j in range(len(bodies)):
        current_gpesum += history[count, j, 3]
        current_kesum += history[count, j, 4]
        
    current_gpesum /= 2 # to avoid double counting energy for the AB system vs. BC system
    
    #instantiate graph points
    ke_point = shapes.Circle((count/history.shape[0])*rendering_size[0], graphing_offset+(current_kesum*50/history.shape[1]),
                            4, 
                            color=red, 
                            batch=graph_batch)
    gpe_point = shapes.Circle((count/history.shape[0])*rendering_size[0], graphing_offset+(current_gpesum*50/history.shape[1]),
                            4, 
                            color=blue, 
                            batch=graph_batch)
    sum_point = shapes.Circle((count/history.shape[0])*rendering_size[0], graphing_offset+((current_gpesum+current_kesum)*50/history.shape[1]),
                            4, 
                            color=white, 
                            batch=graph_batch)
    
    # add to list of graph point objects
    energy.append(ke_point)
    energy.append(gpe_point)
    energy.append(sum_point)
    
    # update labels
    #print('Total Kinetic Energy = %.2f' % current_kesum)
    label_ke.text = 'Total Kinetic Energy = %.4f' % current_kesum
    label_gpe.text = 'Total Gravitational Potential Energy = %.4f' % current_gpesum
    label_sum.text = 'Total Energy = %.4f' % (current_gpesum+current_kesum)

    count += skip
    
    if ss:
        pyglet.image.get_buffer_manager().get_color_buffer().save("./ss/" + str(count)+'.png')

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 0.01, skip)
    pyglet.app.run()
