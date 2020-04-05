from Resources import Rendering
from pyglet.gl import *
from math import *
from Resources.Math import Vector
from collections import deque
from time import time


class LowLevel:
    width = None
    height = None
    active = None

    def __init__(self, window):
        self.top_level = window
        self.mode = 2
        LowLevel.width, LowLevel.height = window.get_size()
        LowLevel.active = self
        self.group = Rendering.Group()
        Rendering.low = self
        self.queue = deque()

    @staticmethod
    def convert_pos(pos):
        if len(pos) == 3:
            x, y, z = pos
            return Vector(-x, y, z)
        return Vector(*pos)

    def setup(self):
        # transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # texture stuff
        glColor3f(1, 1, 1)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    def enable_3d(self):
        width, height = self.top_level.get_size()
        glEnable(GL_DEPTH_TEST)
        viewport = self.top_level.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(70.0, width / float(height), 0.01, 1000.0)  # FOVy, window dimensions, near, far range of view
        glMatrixMode(GL_MODELVIEW)
        self.update_camera_position()
        self.mode = 3

    def update_camera_position(self):
        glLoadIdentity()  # load identity matrix
        x, y = self.top_level.rotation  # retrieve x (sideways turn), and y (updown turn)
        glRotatef(x + 180, 0, 1, 0)  # turn camera to face side direction (for some reason 0 = face neg)
        glRotatef(y, cos(radians(x)), 0, sin(radians(x)))  # rotate up down
        x, y, z = self.top_level.position  # retrieve camera position
        glTranslatef(x, -y, -z)  # move the camera

    def enable_2d(self):
        width, height = self.top_level.get_size()
        glDisable(GL_DEPTH_TEST)
        viewport = self.top_level.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, max(1, width), 0, max(1, height), -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.mode = 2

    def assert_3d(self):
        if self.mode != 3:
            self.enable_3d()

    def assert_2d(self):
        if self.mode != 2:
            self.enable_2d()

    def render(self):
        Rendering._ElementTemplate.default_group.render()

    def process_queue(self, tick=1/20):
        t = time()
        while time() - t < tick and self.queue:
            func, args = self.queue.popleft()
            func(*args)
