import math
from Resources.Math import Vector


class Camera:
    def __init__(self, window):
        self._window = window
        self._hitbox = None
        self._third_person = False
        follow_vector = None
        self.position = 0, 0, 0
        self.rotation = 0, 0

    def move(self, dx, dy, dz):
        x, y, z = self.position
        self.position = x + dx, y + dy, z + dz

    def vision_vector(self):
        side, up = self.rotation
        dx = math.sin(math.radians(side)) * math.cos(math.radians(up))
        dz = math.cos(math.radians(side)) * math.cos(math.radians(up))
        dy = math.sin(math.radians(up))
        return Vector(dx, dy, dz).unit_vector()

    def _establish_hitbox(self, hitbox):
        pass

    @property
    def hitbox(self):
        return self._hitbox

    @hitbox.setter
    def hitbox(self, value):
        pass

    @property
    def third_person(self):
        pass

    @third_person.setter
    def third_person(self, value):
        pass
