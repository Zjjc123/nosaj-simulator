import pyglet
import numpy as np
from pyglet import shapes
from init import *

from constants import *
from colors import distinct_colors
import simulator

# global variables
# window size
rendering_size = [1920, 1080]
rendering_offset = [rendering_size[0]/2, rendering_size[1]/2]
rendering_multiplier = 0

# graph offset
graphing_offset = 200

# graph key font size
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

# initialize other useful things
history = []
ss = False
plot_energy = False
skip = 0
trail_length = 0
settings = {}
colors = []
sizes = []


# instantiate labels
label_ke = pyglet.text.Label('Total Kinetic Energy = %.2f' % 0, font_size = fontsize, x= rendering_size[0]/50, y=graphing_offset*0.1+fontsize*2, color=RED + (255,), batch=text_batch, anchor_x='left')
label_gpe = pyglet.text.Label('Total Gravitational Potential Energy = %.2f' % 0, font_size = fontsize, x= rendering_size[0]/50, y=graphing_offset*0.1+fontsize, color=BLUE + (255,), batch=text_batch, anchor_x='left')
label_sum = pyglet.text.Label('Total Energy = %.2f' % 0, font_size = fontsize, x= rendering_size[0]/50, y=graphing_offset*0.1, color=WHITE + (255,), batch=text_batch, anchor_x='left')

# set count, which tracks the number of timesteps rendered
count = 0

# set up window
window = pyglet.window.Window(width=rendering_size[0], height=rendering_size[1])
window.set_visible(False)

def run_nbody(parsed, args):
    initial = InitialCondition(args['ic'])

    global settings
    if initial == InitialCondition.SIMPLE_TWO_BODY:
        settings = simple_two_body(True)
    if initial == InitialCondition.SUN_EARTH_MOON:
        settings = sun_earth_moon(True)
    if initial == InitialCondition.SOLAR_SYSTEM:
        settings = solar_system(True)

    if parsed.timestep == -1:
        parsed.timestep = settings['timestep']
    if args['ss'] == True:
        global ss
        ss = True
        
    # render scale
    global rendering_multiplier
    rendering_multiplier = settings['multiplier'] * (rendering_size[0]/1280)

    # timestep skipping
    global skip
    skip = parsed.skip

    global trail_length
    trail_length = parsed.trail_length

    global plot_energy
    plot_energy = args['plot_energy']

    # use simulate.py to run nbody
    global history
    history, nbodies = simulator.simulate(parsed.timestep, parsed.iterations, initial)

    global window
    window.set_visible()

    # normalize energy by total energy (min-max normalization)
    total_energy = history[:,:,3] + history[:,:,4]
    total_distance = history[:,:,0] + history[:,:,1] + history[:,:,2]

    history[:,:,0] = history[:,:,0]/(np.max(total_distance)-np.min(total_distance))
    history[:,:,1] = history[:,:,1]/(np.max(total_distance)-np.min(total_distance))
    history[:,:,2] = history[:,:,2]/(np.max(total_distance)-np.min(total_distance))
    history[:,:,3] = history[:,:,3]/(np.max(total_energy)-np.min(total_energy))
    history[:,:,4] = history[:,:,4]/(np.max(total_energy)-np.min(total_energy))

    global colors
    colors = distinct_colors(history.shape[1])

    global sizes
    sizes = settings['sizes']

    global bodies
    # generate objects for each body
    for i in range(history.shape[1]):
        # instantiate new n body circle
        newbody = shapes.Circle(history[0,i,0] * rendering_multiplier+rendering_offset[0],
                                history[0,i,1] * rendering_multiplier+rendering_offset[1],
                                float(sizes[i]), color=colors[i], batch=n_batch)

        bodies.append(newbody)

    global trail
    # instantiate trail
    for i in range(len(bodies)):
            # for each particle in the trail length:
            for j in range(trail_length):
                # instantiate trail object
                newbody = shapes.Circle(history[0,i,0] * rendering_multiplier+rendering_offset[0],
                                        history[0,i,1] * rendering_multiplier+rendering_offset[1],
                                        float(max(4, sizes[i]*((trail_length) - j)/((trail_length))) - 2),  # Jay Pog's big brained formula to normalize size from 4 - 10
                                        color=colors[i],
                                        batch=particle_batch)
                newbody.opacity = 50
                trail.append(newbody)

    pyglet.clock.schedule_interval(update, 0.01, skip)
    pyglet.app.run()

# drawing function
@window.event
def on_draw():
    # clear window
    window.clear()

    # render batches
    particle_batch.draw()
    n_batch.draw()
    if plot_energy:
        graph_batch.draw()
        text_batch.draw()

# update function
def update(dt, skip):
    global count # python global variables

    # N BODIES
    # for each body:
    global bodies
    #print(bodies)
    for i in range(len(bodies)):
        # update position of body objects
        bodies[i].position = (history[count,i,0]*rendering_multiplier+rendering_offset[0], 
                                history[count,i,1] * rendering_multiplier+rendering_offset[1])
                                
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
                trail[j+i*trail_length].position = (history[count-(j*skip),i,0] * rendering_multiplier+rendering_offset[0],
                                        history[count-(j*skip),i,1] * rendering_multiplier+rendering_offset[1])
            else:
                trail[j+i*trail_length].position = (history[count,i,0]*rendering_multiplier+rendering_offset[0], 
                            history[count,i,1] * rendering_multiplier+rendering_offset[1])

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
                            color=RED, 
                            batch=graph_batch)
    gpe_point = shapes.Circle((count/history.shape[0])*rendering_size[0], graphing_offset+(current_gpesum*50/history.shape[1]),
                            4, 
                            color=BLUE, 
                            batch=graph_batch)
    sum_point = shapes.Circle((count/history.shape[0])*rendering_size[0], graphing_offset+((current_gpesum+current_kesum)*50/history.shape[1]),
                            4, 
                            color=WHITE, 
                            batch=graph_batch)
    
    # add to list of graph point objects
    energy.append(ke_point)
    energy.append(gpe_point)
    energy.append(sum_point)
    
    # update labels
    label_ke.text = 'Total Kinetic Energy = %.4f' % current_kesum
    label_gpe.text = 'Total Gravitational Potential Energy = %.4f' % current_gpesum
    label_sum.text = 'Total Energy = %.4f' % (current_gpesum+current_kesum)

    count += skip
    
    if ss:
        pyglet.image.get_buffer_manager().get_color_buffer().save("./ss/" + str(count)+'.png')
    
    if count >= history.shape[0]:
        pyglet.app.exit()
