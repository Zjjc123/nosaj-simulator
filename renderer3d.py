import numpy as np
from init import *

from constants import *
from colors import distinct_colors
import simulator

from direct.showbase.ShowBase import ShowBase
import panda3d
from panda3d.core import Material
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import LVector3
from direct.task import Task
import random, sys, os, math

from math import pi, sin, cos

class Renderer(ShowBase):
    def __init__(self, skip, trail_length, timestep, iterations):
        ShowBase.__init__(self)

        # disable default camera driver
        base.disableMouse()

        # set background color
        base.setBackgroundColor(0,0,0)

        # event handler on left mouse click
        self.accept("mouse1", self.setMouseClick, [True])
        self.accept("mouse1-up", self.setMouseClick, [False])

        self.previous_mouse_x = 0
        self.previous_mouse_y = 0

        self.is_mouse_clicked = False
        self.is_first_click = True

        self.drag_sensitivity = 90

        # event handler on scroll
        self.accept("wheel_up", self.setScroll, [1])
        self.accept("wheel_down", self.setScroll, [-1])

        self.scroll_state = 0

        # zoom constants
        self.zoom_speed = 10
        self.initZoom = 100
        self.zoomInLimit = 5
        self.zoomOutLimit = 1000

        # set up camera to anchor
        self.camAnchor = render.attachNewNode("Cam Anchor") 
        base.camera.reparentTo(self.camAnchor)
        base.camera.setPos(0, -self.initZoom, 0)
        base.camera.lookAt(self.camAnchor)

        # initialize variables
        self.count = 0
        self.skip = skip
        self.trail_length = 40

        # run simulation
        self.history, nbodies = simulator.simulate(timestep, iterations, InitialCondition.SIMPLE_TWO_BODY)
        
        # normalize energy by total energy (min-max normalization)
        total_energy = self.history[:,:,3] + self.history[:,:,4]
        total_distance = self.history[:,:,0] + self.history[:,:,1] + self.history[:,:,2]

        self.history[:,:,0] = self.history[:,:,0]/(np.max(total_distance)-np.min(total_distance))*100
        self.history[:,:,1] = self.history[:,:,1]/(np.max(total_distance)-np.min(total_distance))*100
        self.history[:,:,2] = self.history[:,:,2]/(np.max(total_distance)-np.min(total_distance))*100
        self.history[:,:,3] = self.history[:,:,3]/(np.max(total_energy)-np.min(total_energy))
        self.history[:,:,4] = self.history[:,:,4]/(np.max(total_energy)-np.min(total_energy))

        # get colors and sizes
        self.colors = distinct_colors(self.history.shape[1])
        self.new_colors = []
        for color in self.colors:
            color_elements = []
            for element in color:
                color_elements.append(element/255.0)
            self.new_colors.append(color_elements)
        #self.sizes = settings['sizes']

        # array storing bodies, trails, and energy graphics
        self.bodies = []
        self.trail = []
        self.energy = []

        # generate objects for each body
        for i in range(self.history.shape[1]):
            # generate sphere
            sphere = self.loader.loadModel("models/ball")
            sphere.reparentTo(self.render)
            sphere.setScale(2,2,2)
            sphere.setPos(self.history[0,i,0], self.history[0,i,1], self.history[0,i,2])

            # set material/texture
            m = Material()
            m.setSpecular((1, 1, 1, 1))
            m.setShininess(96)
            sphere.setColor((*self.new_colors[i], 1))
            sphere.setMaterial(m, 1)

            self.bodies.append(sphere)

        # generate objects for trail
        for i in range(self.history.shape[1]):
            # for each particle in the trail length:
            for j in range(self.trail_length):
                # instantiate trail object
                sphere = self.loader.loadModel("models/ball")
                sphere.reparentTo(self.render)
                s = 2*((self.trail_length) - j)/self.trail_length
                sphere.setScale(s,s,s)
                sphere.setPos(self.history[0,i,0], self.history[0,i,1], self.history[0,i,2])
                sphere.set_transparency(panda3d.core.TransparencyAttrib.M_alpha)
                   
                m = Material()
                m.setSpecular((1, 1, 1, 1))
                m.setShininess(96)
                
                sphere.setColor((*self.new_colors[i], 0.3))
                sphere.setMaterial(m, 1)

                self.trail.append(sphere)

        # set up light
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((.55, .55, .55, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(LVector3(0, 0, -1))
        directionalLight.setColor((0.375, 0.375, 0.375, 1))
        directionalLight.setSpecularColor((1, 1, 1, 1))
        self.render.setLight(render.attachNewNode(ambientLight))
        self.render.setLight(render.attachNewNode(directionalLight))

        # Add the update function to the task manager (ran every frame).
        self.taskMgr.add(self.update, "updateTask")

        # Add the camera functions to the task manager
        self.taskMgr.add(self.camera_orbit_task, "orbitTask")
        self.taskMgr.add(self.scroll_zoom_task, "zoomTask")

    # update task
    def update(self, task):
        if self.count < self.history.shape[0]:
            for i in range(self.history.shape[1]):
                # update positions of bodies
                self.bodies[i].setPos(self.history[self.count,i,0], self.history[self.count,i,1], self.history[self.count,i,2])

                # update positions of trail
                for j in range(self.trail_length):   
                    if self.skip*j <self.count:
                        self.trail[j+i*self.trail_length].setPos(self.history[self.count-(j*self.skip),i,0],
                                                self.history[self.count-(j*self.skip),i,1], self.history[self.count-(j*self.skip),i,2])
            self.count += self.skip  
        return task.cont

    # task to orbit camera when dragged
    def camera_orbit_task(self, task):
        if self.is_mouse_clicked:
            # if this is the first click reset previous position tracker
            if self.is_first_click:
                if base.mouseWatcherNode.hasMouse():
                    self.previous_mouse_x = base.mouseWatcherNode.getMouseX()
                    self.previous_mouse_y = base.mouseWatcherNode.getMouseY()
                    self.is_first_click = False

            if base.mouseWatcherNode.hasMouse():
                mouse_x = base.mouseWatcherNode.getMouseX()
                mouse_y = base.mouseWatcherNode.getMouseY()

                # calculate mouse change
                delta_mouse_x = (self.previous_mouse_x - mouse_x) * self.drag_sensitivity
                delta_mouse_y = (self.previous_mouse_y - mouse_y) * self.drag_sensitivity
                
                # find new rotation of the anchor relative camera
                newH = self.camAnchor.getH(self.camera) + delta_mouse_x 
                newP = self.camAnchor.getP(self.camera) + -delta_mouse_y

                self.camAnchor.setHpr(self.camera, newH, newP, 0)

                self.previous_mouse_x = mouse_x
                self.previous_mouse_y = mouse_y

        return task.cont
    
    # task to zoom in and out based on scroll wheel
    def scroll_zoom_task(self, task):
        # get new location based on the scroll and zoom
        newY = (base.camera.getY() + self.scroll_state * self.zoom_speed)

        # limit zoom
        if(newY > -self.zoomInLimit): newY = -self.zoomInLimit
        if(newY < -self.zoomOutLimit): newY = -self.zoomOutLimit

        base.camera.setY(newY)

        # reset scroll state
        self.scroll_state = 0
        return task.cont

    # set mouse click state (true = down, false = not down)
    def setMouseClick(self, value):
        if not value:
            self.is_first_click = True
        self.is_mouse_clicked = value

    # set scroll state (0 = no movement, 1 = up, -1 = down)
    def setScroll(self, value):
        self.scroll_state = value

app = Renderer(50, 40, 0.0001, 40000)
app.run()