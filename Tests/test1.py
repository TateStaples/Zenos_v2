from Zenos_package import *


class TestWindow(Window):
    head = ThreeD.Sphere((0, 2, 0), 0.5, WHITE)
    body = ThreeD.Cone((0, 0, 0), 0.5, 1.75, WHITE)
    pawn = ThreeD.Combination(head, body)

    def periodic(self, dt: float):
        super(TestWindow, self).periodic(dt)
        if self.is_pressed(self.keys.R):
            self.pawn.move(0, dt, 0)


if __name__ == '__main__':
    x = TestWindow()
    x.start()
