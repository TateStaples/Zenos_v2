from Zenos_package import *


class TestWindow(Window):  # basic 3d Tests
    c = ThreeD.Cube((0, 0, 0), 10, Color(255, 0, 0, 255))
    text = TwoD.Text((100, 100), "", 30)
    # origin = ThreeD.Cube((0, 0, 0), .1, Color(0, 255, 0, 255))

    def __init__(self):
        super(TestWindow, self).__init__()
        self.move_camera(0, 0, -30)
        self.add_collidable(self.c)

    def periodic(self, dt):
        super(TestWindow, self).periodic(dt)
        self.text.set_string(self.c.distance(self.position))
        self.render(self.text)


if __name__ == '__main__':
    x = TestWindow()
    # x.set_background(LIGHT_BLUE)
    x.lock_mouse()
    x.start()