import pyglet
import numpy as np
from pyglet import shapes

import simulator

window = pyglet.window.Window(width=1280, height=720)
batch = pyglet.graphics.Batch()

bodies = []
history = simulator.simulate(0.0001, 100000)
count = 0

rendering_multplier = 200
rendering_offset = [640, 360]

for i in range(history.shape[1]):
    newbody = shapes.Circle(history[0,i,0]*rendering_multplier+rendering_offset[0],history[0,i,1]*rendering_multplier+rendering_offset[1],10,color=(50, 225, 30), batch=batch)
    bodies.append(newbody)
    print(history[0,i,0]*rendering_multplier+rendering_offset[0], history[0,i,1]*rendering_multplier+rendering_offset[1])

@window.event
def on_draw():
    window.clear()
    batch.draw()

def update(dt, skip):
    global count
    for i in range(len(bodies)):
        bodies[i].position = (history[count,i,0]*rendering_multplier+rendering_offset[0],history[count,i,1]*rendering_multplier+rendering_offset[1])
    count += skip
    # pyglet.image.get_buffer_manager().get_color_buffer().save("./ss/" + str(count)+'.png')

if __name__ == '__main__':
    skip = 100
    pyglet.clock.schedule_interval(update, 0.01, skip)
    pyglet.app.run()
