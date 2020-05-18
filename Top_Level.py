
import pyglet
from Low_Level import LowLevel
import math
from pyglet.window.key import *
from Resources.Overlays import BLACK, Color
from Resources.Rendering import Group
from Resources.Math import Vector


class Window(pyglet.window.Window):
    active_window = None
    keys = pyglet.window.key

    def __init__(self):
        super(Window, self).__init__(resizable=True)
        Window.active_window = self
        pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MIN_FILTER, pyglet.gl.GL_NEAREST)
        pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
        self.rotation = 0, 0
        self.position = 0, 0, 0
        self.mode = 2
        self.bg_color = BLACK
        self._inner = LowLevel(self)
        self.turn_sensivity = 10  # 1-100 = pixels mouse moves per degree of rotation
        self.mouse_locked = False
        self.key_checker = KeyStateHandler()
        self.push_handlers(self.key_checker)
        self._is_fog = False
        self.speed = 20
        self.colliables = []

    def start(self):
        self._inner.setup()
        self.process_entire_queue()
        pyglet.clock.schedule_interval(self.periodic, 1 / 120.0)
        pyglet.app.run()

    def periodic(self, dt: float):
        self._inner.process_queue()
        if self.is_pressed(DOWN) or self.is_pressed(S):
            self.move_forward(-dt * self.speed)
        elif self.is_pressed(UP) or self.is_pressed(W):
            self.move_forward(dt * self.speed)
        elif self.is_pressed(RIGHT) or self.is_pressed(D):
            self.move_sideways(dt * self.speed)
        elif self.is_pressed(LEFT) or self.is_pressed(A):
            self.move_sideways(-dt * self.speed)
        self.render_shown()

    def render(self, *args):
        for item in args:
            try:
                if type(item) == Group:
                    item.render()
                elif item.dimension == 2:
                    self._inner.assert_2d()
                    item.render()
                elif item.dimension == 3:
                    self._inner.assert_3d()
                    item.render()
                else:
                    print(f"**invalid item rendered: {item}")
                    quit()
            except NameError:
                print("The item you tried to render was not valid")
                self.quit()

    def render_shown(self):
        self.clear()
        self._inner.render()

    def draw_all(self):
        self._inner.assert_2d()
        for item in self._draw_items2:
            item.render()
        self._inner.enable_3d()
        for item in self._draw_items3:
            item.render()

    def on_mouse_motion(self, x, y, dx, dy):  # default will be altering camera view
        if self.mouse_locked:
            side, up = self.rotation
            theta_y = dy * self.turn_sensivity/100
            theta_x = dx * self.turn_sensivity/100
            self.rotation = side + theta_x, up + theta_y
            self._inner.update_camera_position()

    def set_background(self, color: Color):
        self.bg_color = color
        pyglet.gl.glClearColor(*[i/255 for i in color.raw()])

    def lock_mouse(self, should=True):
        self.mouse_locked = should
        self.set_exclusive_mouse(should)

    def move_forward(self, dis, planar=False):
        if planar:
            dx, dy, dz = self.vision_vector()
            move = Vector(dx, 0, dz).unit_vector() * dis
        else:
            move = Vector(self.vision_vector() * dis)

        for collidable in self.colliables:
            move = collidable.do_collision
        self.position = x + dx, y + dy, z + dz
        self._inner.update_camera_position()

    def move_sideways(self, dis):
        side, up = self.rotation
        side += 90
        dx = math.sin(math.radians(side)) * dis
        dz = math.cos(math.radians(side)) * dis
        dy = 0  # math.sin(math.radians(up)) * dis
        x, y, z = self.position
        self.position = x + dx, y + dy, z + dz
        self._inner.update_camera_position()

    def is_pressed(self, key):
        return self.key_checker[key]

    def set_fog(self, should=True, start_dis=20, depth=40):
        if should:
            # Enable fog. Fog "blends a fog color with each rasterized pixel fragment's
            # post-texturing color."
            pyglet.gl.glEnable(pyglet.gl.GL_FOG)
            # Set the fog color.
            pyglet.gl.glFogfv(pyglet.gl.GL_FOG_COLOR, (pyglet.gl.GLfloat * 4)(*self.bg_color.raw()))
            # Say we have no preference between rendering speed and quality.
            pyglet.gl.glHint(pyglet.gl.GL_FOG_HINT, pyglet.gl.GL_DONT_CARE)
            # Specify the equation used to compute the blending factor.
            pyglet.gl.glFogi(pyglet.gl.GL_FOG_MODE, pyglet.gl.GL_LINEAR)
            # How close and far away fog starts and ends. The closer the start and end,
            # the denser the fog in the fog range.
            pyglet.gl.glFogf(pyglet.gl.GL_FOG_START, start_dis)
            pyglet.gl.glFogf(pyglet.gl.GL_FOG_END, start_dis+depth)
        else:
            pyglet.gl.glDisable(pyglet.gl.GL_FOG)

    def queue(self, function_or_class, args):
        self._inner.queue.append((function_or_class, args))

    def process_entire_queue(self):
        self._inner.process_queue(20)

    def vision_vector(self):
        side, up = self.rotation
        dx = math.sin(math.radians(side)) * math.cos(math.radians(up))
        dz = math.cos(math.radians(side)) * math.cos(math.radians(up))
        dy = math.sin(math.radians(up))
        return Vector(dx, dy, dz).unit_vector()

    def move_camera(self, dx, dy, dz):
        x, y, z = self.position
        self.position = x + dx, y + dy, z + dz

    def add_collidable(self, obj):
        self.colliables.append(obj)