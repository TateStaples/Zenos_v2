from Zenos_package import *
import pyglet

class TestWindow(Window):
    c = TwoD.Square((500, 100), 100, Color(255, 0, 0, 128))
    c2 = TwoD.Square((0, 100), 100, Color(0, 255, 0, 255))

    def start(self):
        self.c.put_on_top()
        super(TestWindow, self).start()

    def periodic(self, dt: float):
        super(TestWindow, self).periodic(dt)
        # glClear(GL_COLOR_BUFFER_BIT)
        # self.render(self.c2, self.c)

    def on_mouse_motion(self, x, y, dx, dy):
        self.c.moveTo((x, y))


if __name__ == '__main__':
    x = TestWindow()
    x.start()
