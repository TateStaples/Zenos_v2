from Zenos_package import *
from Physics import Physical

class GameWindow(Window):
    planar = True
    ball = Physical(ThreeD.Sphere((0, 2, 3), 1, Gradient(RED, BLUE, "horizontal")), do_grav=True, intial_velocity=Vector(0, -.1, 0))
    running_physics = True

    def __init__(self):
        super(GameWindow, self).__init__()
        self.position = 0, 4, -5
        self.establish_walls()
        self.add_hitbox(Physical(ThreeD.RectPrism((0, -1.5, 5), 0.5, 0.5, 2, RED), momentum=False, do_grav=True))

    def establish_walls(self):
        width = 50
        wall_height = 10
        self.floor = Physical(ThreeD.RectPrism((0, -1, 0), width * 2, width * 2, 2, GREEN), moveable=False)
        self.wall1 = Physical(ThreeD.RectPrism((width, wall_height / 2, 0), width * 2, 2, wall_height, GREY), moveable=False)
        self.wall2 = Physical(ThreeD.RectPrism((-width, wall_height / 2, 0), width * 2, 2, wall_height, GREY), moveable=False)
        self.wall3 = Physical(ThreeD.RectPrism((0, wall_height / 2, width), 2, width * 2, wall_height, GREY), moveable=False)
        self.wall4 = Physical(ThreeD.RectPrism((0, wall_height / 2, -width), 2, width * 2, wall_height, GREY), moveable=False)

if __name__ == '__main__':
    t = GameWindow()
    t.lock_mouse()
    t.set_background(LIGHT_BLUE)
    t.start()