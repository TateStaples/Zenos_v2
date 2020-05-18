from Zenos_package import *


class GameWindow(Window):
    planar = True

    def __init__(self):
        super(GameWindow, self).__init__()
        self.position = 0, 2, 0
        self.establish_walls()
        self.establish_collisions()

    def establish_walls(self):
        width = 50
        wall_height = 10
        self.floor = ThreeD.RectPrism((0, -1, 0), width * 2, width * 2, 2, BROWN)
        self.wall1 = ThreeD.RectPrism((width, wall_height / 2, 0), width * 2, 2, wall_height, GREY)
        self.wall2 = ThreeD.RectPrism((-width, wall_height / 2, 0), width * 2, 2, wall_height, GREY)
        self.wall3 = ThreeD.RectPrism((0, wall_height / 2, width), 2, width * 2, wall_height, GREY)
        self.wall4 = ThreeD.RectPrism((0, wall_height / 2, -width), 2, width * 2, wall_height, GREY)

    def establish_collisions(self):
        self.add_collidable(self.wall1, self.wall2, self.wall3, self.wall4)

if __name__ == '__main__':
    t = GameWindow()
    t.lock_mouse()
    t.set_background(LIGHT_BLUE)
    t.start()