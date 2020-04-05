from Zenos_package import *


class TestWindow(Window):  # basic 3d Tests
    c = ThreeD.Sphere((0, 0, 0), 10, Color(255, 0, 0, 255))
    # origin = ThreeD.Cube((0, 0, 0), .1, Color(0, 255, 0, 255))

    def __init__(self):
        super(TestWindow, self).__init__()

    def periodic(self, dt):
        super(TestWindow, self).periodic(dt)
        # self.c.move(pitch=10*dt, yaw=20*dt, roll=50*dt)


if __name__ == '__main__':
    x = TestWindow()
    # x.set_background(LIGHT_BLUE)
    x.lock_mouse()
    x.start()