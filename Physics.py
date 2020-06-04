from Resources.Math import Vector, distance
from Resources.Rendering import _ElementTemplate
from copy import deepcopy
from math import *

'''
Units:
distance = meters
time = seconds
force = N
mass = kg
'''


class Physical:
    standard_grav = Vector(0, -10, 0)
    air_resistance = 1
    gravitational_constant = 6.674e-11  # in standard units above
    all_objects = []

    def __init__(self, shape: _ElementTemplate, intial_velocity: Vector = None, mass: float = 1,
                 do_standard_grav: bool = True, momentum: bool = True, friction_coefficient: float = 0.5,
                 moveable: bool = True, do_grav: bool = True, do_collisions: bool = True):
        self.do_standard_gravity = do_standard_grav
        self.velocity = intial_velocity if intial_velocity is not None else Vector([0 for i in range(shape.dimension)])
        self.shape = shape
        self.do_momentum = momentum
        self.all_objects.append(self)
        self.friction_coefficient = friction_coefficient
        self.mass = mass
        self.moveable = moveable
        self.affected_by_gravity = do_grav

    def do_collision(self, other, dt):
        trans = self.velocity * dt
        if trans.magnitude() == 0:
            return
        new_pos = Vector(self.shape.location) + trans
        if self.shape.distance(other.shape) < 0:
            perp = Vector.from_2_points(self.shape.get_nearest_point(other.shape.location),
                                        other.shape.get_nearest_point(self.shape.location))  # this is vector up to wall
            dis_traveled = trans.magnitude()  # full dis travelled in this increment
            theta = perp.angle_to(trans)
            perp2 = deepcopy(perp)  # this is the perp compoent of the initial trans
            perp2.resize(cos(radians(theta)) * dis_traveled)  # this resizes it to the prwoper length
            horizontal = Vector.from_2_points(perp2 + self.shape.location,
                                              new_pos)  # this find the component of initial trans parallel to wall
            # horizontal contains a dis, make into vector
            print(self.velocity)
            self.velocity = perp + horizontal
            print("collide:", self, other, self.velocity)
            if self.do_momentum:
                acceleration = (perp2 - perp) / dt  # acceleration is change in velocity over time
                push_force = self.get_acceleration_force(acceleration)
                friction = push_force * self.friction_coefficient
                self.apply_force(friction, dt)
                other.apply_force(push_force, dt)

    def get_momentum(self):
        return self.velocity * self.mass

    def update(self, dt):
        if not self.moveable:
            return
        if self.affected_by_gravity:
            self.apply_gravity(dt)
        for obj in self.all_objects:
            if obj is not self:
                self.do_collision(obj, dt)
        self.shape.move(*(self.velocity * dt))
        if not self.do_momentum:
            self.velocity = self.velocity * 0

    def apply_gravity(self, dt):
        if self.do_standard_gravity:
            self.velocity = self.velocity + self.standard_grav * dt
        else:
            for obj in self.all_objects:
                if obj is not self:
                    f = self.get_gravitational_force(obj)
                    self.apply_force(f, dt)

    def apply_force(self, force, dt):
        acceleration = force / self.mass
        self.velocity = self.velocity + acceleration * dt

    def get_gravitational_force(self, other):
        dis = distance(self.shape.location, other.shape.location)
        return self.gravitational_constant * self.mass * other.mass / (dis * dis)

    def get_acceleration_force(self, acceleration: float):
        return acceleration * self.mass

    def __repr__(self):
        return str(self.shape)