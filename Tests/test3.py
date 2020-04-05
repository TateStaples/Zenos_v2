from Zenos_package import *
import random

class TestWindow(Window):
    def __init__(self):
        super(TestWindow, self).__init__()
        self.ground = ThreeD.RectPrism((0, -2, 0), 100, 1000, 1, BROWN)
        self.ground.show()
        self.cubes = []
        for i in range(100):
            c = self.create_cube()
            c.show()
            self.cubes.append(c)

    def periodic(self, dt):
        super(TestWindow, self).periodic(dt)
        for item in self.cubes:
            dt *= 1
            v = Vector.from_2_points(item.location, self.position)
            item.move(*v.unit_vector() * dt)
        # self.c1.move(dt, 0, 0)

    @staticmethod
    def create_cube():
        pos = random.randint(-50, 50), random.randint(0, 50), random.randint(-50, 50)
        overlay = Gradient(random.choice(Color.previously_made), random.choice(Color.previously_made))
        return ThreeD.Cube(pos, 1, overlay)


if __name__ == '__main__':
    x = TestWindow()
    x.set_background(LIGHT_GREY)
    x.lock_mouse()
    x.start()
