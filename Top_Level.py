import pyglet
from Low_Level import LowLevel
import math
from pyglet.window.key import *
from Resources.Overlays import BLACK, Color
from Resources.Rendering import Group
from Resources.Math import Vector, rotate_3d
from Physics import Physical


class Window(pyglet.window.Window):
    active_window = None
    keys = pyglet.window.key
    planar = True
    running_physics = False

    # setup
    def __init__(self):
        super(Window, self).__init__(resizable=True)
        Window.active_window = self
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
        self.speed = 10
        self.velocity = Vector(0, 0, 0)
        self.colliables = []
        self.hitbox = None
        self.third_person = False

    def start(self):
        self._inner.setup()
        self.process_entire_queue()
        pyglet.clock.schedule_interval(self.periodic, 1 / 120.0)
        pyglet.app.run()

    # game loop
    def periodic(self, dt: float):
        self._inner.process_queue()
        self.check_user_input()
        self.move(dt)
        if self.hitbox is None:  # else use the hitbox momentum variable
            self.velocity = Vector(0, 0, 0)
        if self.running_physics:
            for obj in Physical.all_objects:
                if obj is not self.hitbox:
                    obj.update(dt)
        self.render_shown()

    # draw functions
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
                    self.quit()
            except NameError:
                print("The item you tried to render was not valid")
                self.quit()

    def render_shown(self):
        self.clear()
        self._inner.render()

    # mouse functions
    def on_mouse_motion(self, x, y, dx, dy):  # default will be altering camera view
        if self.mouse_locked:
            side, up = self.rotation
            theta_y = dy * self.turn_sensivity/100
            theta_x = dx * self.turn_sensivity/100
            self.rotation = side + theta_x, up + theta_y
            if self.hitbox is not None and self.third_person:
                self.position = rotate_3d([self.position], self.hitbox.shape.location, theta_y, 0, -theta_x)[0]
            # self._inner.update_camera_position()

    def lock_mouse(self, should=True):
        self.mouse_locked = should
        self.set_exclusive_mouse(should)

    def is_pressed(self, key):
        return self.key_checker[key]

    def vision_vector(self):
        side, up = self.rotation
        dx = math.sin(math.radians(side)) * math.cos(math.radians(up))
        dz = math.cos(math.radians(side)) * math.cos(math.radians(up))
        dy = math.sin(math.radians(up))
        return Vector(dx, dy, dz).unit_vector()

    # movement
    def check_user_input(self):
        if self.is_pressed(DOWN) or self.is_pressed(S):
            self.move_forward(-self.speed)
        elif self.is_pressed(UP) or self.is_pressed(W):
            self.move_forward(self.speed)
        if self.is_pressed(RIGHT) or self.is_pressed(D):
            self.move_sideways(self.speed)
        elif self.is_pressed(LEFT) or self.is_pressed(A):
            self.move_sideways(-self.speed)

    def move(self, dt):
        if self.hitbox is not None:
            old_pos = self.hitbox.shape.location
            self.hitbox.velocity = self.velocity
            self.hitbox.update(dt)
            trans = Vector.from_2_points(old_pos, self.hitbox.shape.location)
            self.position = tuple(trans + self.position)
            self.velocity = self.hitbox.velocity
        else:
            self.velocity *= dt
            self.position = tuple(self.velocity + self.position)

    def move_forward(self, dis):
        if self.planar:
            dx, dy, dz = self.vision_vector()
            move = Vector(dx, 0, dz).unit_vector() * dis + self.velocity
        else:
            move = self.vision_vector() * dis + self.velocity

        self.velocity = move
        # self._inner.update_camera_position()

    def move_sideways(self, dis):
        side, up = self.rotation
        side += 90
        dx = math.sin(math.radians(side)) * dis
        dz = math.cos(math.radians(side)) * dis
        dy = 0  # math.sin(math.radians(up)) * dis
        move = Vector(dx, dy, dz) + self.velocity

        self.velocity = move
        # self._inner.update_camera_position()

    def move_camera(self, dx, dy, dz):
        x, y, z = self.position
        self.position = x + dx, y + dy, z + dz

    # buffered loading
    def queue(self, function_or_class, args):
        self._inner.queue.append((function_or_class, args))

    def process_entire_queue(self):
        self._inner.process_queue(20)

    # background affects
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

    def set_background(self, color: Color):
        self.bg_color = color
        pyglet.gl.glClearColor(*[i/255 for i in color.raw()])

    # hitbox for camera
    def add_hitbox(self, physical):
        if physical.shape.dimension == 3:
            physical.shape.move(*self.position)
        self.hitbox = physical
        self.third_person = physical.shape.distance(self.position) > 0