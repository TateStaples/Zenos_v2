from Zenos_package import *
from Physics import Physical

class GameWindow(Window):
    planar = True

    def __init__(self):
        super(GameWindow, self).__init__()
        self.position = 0, 2.1, 0
        self.add_hitbox(Physical(ThreeD.RectPrism((0, 1, 0), 0.5, 0.5, 2, CLEAR)))
        # self.hitbox.fall = False
        self.establish_walls()
        # self.establish_collisions()
        self.grav_stength = 5
        self.gravity = Vector(0, -self.grav_stength, 0)
        self.previous_pos = self.position

    def establish_walls(self):
        width = 50
        wall_height = 50
        self.floor = Physical(ThreeD.RectPrism((0, -1, 0), width * 2, width * 2, 2, BROWN), moveable=False)
        self.wall1 = Physical(ThreeD.RectPrism((width, wall_height / 2, 0), width * 2, 2, wall_height, GREY), moveable=False)
        self.wall2 = Physical(ThreeD.RectPrism((-width, wall_height / 2, 0), width * 2, 2, wall_height, GREY), moveable=False)
        self.wall3 = Physical(ThreeD.RectPrism((0, wall_height / 2, width), 2, width * 2, wall_height, GREY), moveable=False)
        self.wall4 = Physical(ThreeD.RectPrism((0, wall_height / 2, -width), 2, width * 2, wall_height, GREY), moveable=False)
        
    def periodic(self, dt: float):
        self.hitbox.standard_gravity = self.gravity
        dv = Vector.from_2_points(self.previous_pos, self.position)
        self.velocity = self.gravity * dt + dv * 0.95
        self.previous_pos = self.position
        super(GameWindow, self).periodic(dt)
        self.render(TwoD.Text((0, 0), str(self.position), 40, BLACK))
        
    def on_key_press(self, symbol, modifiers):
        super(GameWindow, self).on_key_press(symbol, modifiers)
        if symbol == self.keys.G:
            self.gravity = self.vision_vector() * 10
        elif symbol == self.keys.R:
            self.gravity = Vector(0, -self.grav_stength, 0)
        elif symbol == self.keys.T:
            self.gravity = Vector(0, 0, 0)
            self.velocity = Vector(0, 0, 0)
            self.hitbox.velocity = self.velocity
            self.position = 0, 10, 0


if __name__ == '__main__':
    t = GameWindow()
    t.lock_mouse()
    t.set_background(LIGHT_BLUE)
    t.start()