from Zenos_package import *
import random

class TestWindow(Window):
    test = Texture("/Users/22staples/PycharmProjects/Zenos_v2/files/texture.png", (.25, .25, .25, .25))

    def __init__(self):
        super(TestWindow, self).__init__()
        self.cubes = []
        for x in range(-50, 50):
            for z in range(-50, 50):
                c = ThreeD.Cube((x, -1, z), 1, self.test)
                c.show()
                self.cubes.append(c)


if __name__ == '__main__':
    x = TestWindow()
    x.set_background(LIGHT_BLUE)
    x.lock_mouse()
    x.set_fog(dis=10)
    x.start()
