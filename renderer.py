import pyglet
import numpy as np
from pyglet import shapes

import simulator

rendering_multplier = 200
rendering_offset = [640, 360]

window = pyglet.window.Window(width=1280, height=720)
batch = pyglet.graphics.Batch()
particle_batch = pyglet.graphics.Batch()

bodies = []
trail = []

history = simulator.simulate(0.0001, 100000)

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
    particles = min((skip*40), count+1)
    
    for i in range(len(bodies)):
        for j in range(particles):
            if j % skip == 0:
                newbody = shapes.Circle(history[count-j-1,i,0] * rendering_multplier+rendering_offset[0],
                                        history[count-j-1,i,1] * rendering_multplier+rendering_offset[1],
                                        float(max(4, 10*(particles - j)/(particles)) - 2), 
                                        color=(144, 238, 144), 
                                        batch=particle_batch)
                trail.append(newbody)
  
    count += skip
    # pyglet.image.get_buffer_manager().get_color_buffer().save("./ss/" + str(count)+'.png')

if __name__ == '__main__':
    skip = 100
    pyglet.clock.schedule_interval(update, 0.01, skip)
    pyglet.app.run()
