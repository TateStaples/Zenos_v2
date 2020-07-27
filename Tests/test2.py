from Zenos_package import *
from Physics import Physical
import pyglet


class TestWindow(Window):  # basic 3d Tests
    c = ThreeD.Cone(pos=(0, 0, 0), base_radius=3, height=10, overlay=RED)
    c2 = ThreeD.Cube((0, 0, 0), 1, ORANGE)
    # line = TwoD.Line((0, 0, 0), (50, 50, 0), WHITE)
    # line = TwoD.Square((10, 10, 0), 10, WHITE)
    planar = False
    # origin = ThreeD.Cube((0, 0, 0), .1, Color(0, 255, 0, 255))

    def __init__(self):
        super(TestWindow, self).__init__()
        v = Vector(1, 0, 1)
        x, y, z = v.unit_vector()
        print(v.get_angle())
        a, b, c = v.get_angle()
        up = degrees(asin(z/sqrt(2))) if x > 0 else 360-degrees(asin(z/sqrt(2)))
        side = degrees(asin(x/sqrt(2))) if y > 0 else 360-degrees(asin(x/sqrt(2)))
        print(x, y, z)
        print(up, side)
        self.c.moveTo(0, 0, 0, 0, b, 90+c)
        self.position = 0, 0, -30
        self.s = ThreeD.Sphere(tuple(v.unit_vector()*10), 1, LIGHT_BLUE)
        print(self.c.location)
        print(self.c.vertices[1], self.s.location)

    def on_key_press(self, symbol, modifiers):
        super(TestWindow, self).on_key_press(symbol, modifiers)
        if symbol == self.keys._1:
            self.c.move(0,0,0, 5)
            print(self.c.vertices[1])
        if symbol == self.keys._2:
            self.c.move(0,0,0, 0, 5)
            print(self.c.vertices[1])
        if symbol == self.keys._3:
            self.c.move(0,0,0, 0, 0, 5)
            print(self.c.vertices[1])


if __name__ == '__main__':
    x = TestWindow()
    # x.set_background(LIGHT_BLUE)
    x.lock_mouse()
    x.start()