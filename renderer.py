import pyglet
import numpy as np
from pyglet import shapes

import simulator

rendering_multplier = 200
rendering_size = [1280, 720]
rendering_offset = [rendering_size[0]/2, rendering_size[1]/2]

skip = 100

graphing_offset = 200

window = pyglet.window.Window(width=rendering_size[0], height=rendering_size[1])
batch = pyglet.graphics.Batch()
particle_batch = pyglet.graphics.Batch()

bodies = []
trail = []
energy = []

history = simulator.simulate(0.0001, 100000)
total_energy = history[:,:,3] + history[:,:,4]
history[:,:,3] = history[:,:,3]/(np.max(total_energy)-np.min(total_energy))
history[:,:,4] = history[:,:,4]/(np.max(total_energy)-np.min(total_energy))

count = 0

for i in range(history.shape[1]):
    newbody = shapes.Circle(history[0,i,0] * rendering_multplier+rendering_offset[0],
                            history[0,i,1] * rendering_multplier+rendering_offset[1],
                            10, color=(50, 225, 30), batch=batch)
    bodies.append(newbody)
    print(history[0,i,0]*rendering_multplier+rendering_offset[0], history[0,i,1]*rendering_multplier+rendering_offset[1])

@window.event
def on_draw():
    window.clear()
    particle_batch.draw()
    batch.draw()

def update(dt, skip):
    global count
    for i in range(len(bodies)):
        bodies[i].position = (history[count,i,0]*rendering_multplier+rendering_offset[0], 
                                history[count,i,1] * rendering_multplier+rendering_offset[1])

    global trail
    trail = []
    particles = min((skip*40), count+1) # trail
    
    for i in range(len(bodies)):
        for j in range(particles):
            if j % skip == 0:
                newbody = shapes.Circle(history[count-j-1,i,0] * rendering_multplier+rendering_offset[0],
                                        history[count-j-1,i,1] * rendering_multplier+rendering_offset[1],
                                        float(max(4, 10*(particles - j)/(particles)) - 2), 
                                        color=(144, 238, 144), 
                                        batch=particle_batch)

                trail.append(newbody)
    global energy
    energy = []
    for i in range(count):
        kesum = 0
        gpesum = 0

        if i % skip == 0:    

            for j in range(len(bodies)):
                gpesum += history[i, j, 3]
                kesum += history[i, j, 4]

            ke_point = shapes.Circle((i/history.shape[0])*rendering_size[0], graphing_offset+(kesum*100000/particles),
                                    5, 
                                    color=(255, 0, 0), 
                                    batch=particle_batch)
            gpe_point = shapes.Circle((i/history.shape[0])*rendering_size[0], graphing_offset+(gpesum*100000/particles),
                                    5, 
                                    color=(0, 0, 255), 
                                    batch=particle_batch)

            #print(gpesum)
            #print(kesum)
                                
            energy.append(ke_point)
            energy.append(gpe_point)

        

    count += skip
    pyglet.image.get_buffer_manager().get_color_buffer().save("./ss/" + str(count)+'.png')

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 0.01, skip)
    pyglet.app.run()
