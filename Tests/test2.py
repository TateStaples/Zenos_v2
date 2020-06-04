from Zenos_package import *
from Physics import Physical


class TestWindow(Window):  # basic 3d Tests
    c = Physical(ThreeD.Cube((0, 0, 0), 10, Color(255, 0, 0, 255)))
    text = TwoD.Text((100, 100), "", 30)
    planar = False
    # origin = ThreeD.Cube((0, 0, 0), .1, Color(0, 255, 0, 255))

    def __init__(self):
        super(TestWindow, self).__init__()
        self.position = 0, 0, -30
        self.add_hitbox(Physical(ThreeD.RectPrism((0, 1, 0), 0.5, 0.5, 2, CLEAR), do_grav=False, momentum=False))

    def periodic(self, dt):
        dis = self.c.shape.distance(self.position)
        print(dis)
        super(TestWindow, self).periodic(dt)
        self.text.set_string(self.c.shape.distance(self.position))
        self.render(self.text)


if __name__ == '__main__':
    x = TestWindow()
    x.set_background(LIGHT_BLUE)
    x.lock_mouse()
    x.start()