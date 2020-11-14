from Zenos_package import *
import random


class Boid:
    are_predators = False
    _figure = ThreeD.Cone
    all_boids = []
    color = GREEN

    # bounding box
    box_length = 80
    box_width = 80
    box_height = 80

    ThreeD.RectPrism.mode = pyglet.gl.GL_LINES
    box = ThreeD.RectPrism((0, 0, 0), box_length*2, box_width*2, box_height*2, WHITE)

    # configs
    max_velocity = 70
    visual_range = 20
    coherence_weight = 0.008
    alignment_weight = 0.3
    separation_weight = 0.05
    predator_weight = 0.4

    def __init__(self):
        self.all_boids.append(self)
        self.motion_vector = Vector(random.random()*10-5, random.random()*10-5, random.random()*10-5)
        self.shape = self._figure(pos=(random.randint(-self.box_width+10, self.box_width - 10),
                                  random.randint(-self.box_height+10, self.box_height - 10),
                                  random.randint(-self.box_length+10, self.box_length - 10)),
                                  base_radius=1, height=2, overlay=self.color)

    def get_neighbors(self):
        b = []
        for boid in self.all_boids:
            if boid is not self and distance(boid.shape.location, self.shape.location) < self.visual_range:
                b.append(boid)
        return b

    def cohesion(self):
        c_vector = Vector(0, 0, 0)
        num_neighbors = 0

        for boid in self.get_neighbors():
            c_vector = c_vector + Vector.from_2_points(self.shape.location, boid.shape.location)
            num_neighbors += 1
        return c_vector / num_neighbors * self.coherence_weight if num_neighbors > 0 else c_vector

    def alignment(self):
        neighbors = self.get_neighbors()
        alignment_vector = Vector(0, 0, 0)
        for b in neighbors:
            alignment_vector = alignment_vector + b.motion_vector
        return alignment_vector / len(neighbors) * self.alignment_weight if len(neighbors) > 0 else alignment_vector

    def separation(self):
        neighbors = self.get_neighbors()
        separation_vector = Vector(0, 0, 0)
        for b in neighbors:
            separation_vector = separation_vector - Vector.from_2_points(self.shape.location, b.shape.location)
        return separation_vector / len(neighbors) * self.separation_weight if len(neighbors) > 0 else separation_vector

    def avoid_walls(self):
        avoidance_dis = 20
        strength = 3
        x, y, z = self.shape.location
        avoid_vector = Vector(0, 0, 0)
        if x < avoidance_dis - self.box_width:
            avoid_vector[0] = strength
        elif x > self.box_width - avoidance_dis:
            avoid_vector[0] = -strength
        if y < avoidance_dis - self.box_height:
            avoid_vector[1] = strength
        elif y > self.box_height - avoidance_dis:
            avoid_vector[1] = -strength
        if z < avoidance_dis - self.box_length:
            avoid_vector[2] = strength
        elif z > self.box_length - avoidance_dis:
            avoid_vector[2] = -strength
        return avoid_vector

    def predators(self):
        predator_vector = Vector(0, 0, 0)
        num_preds = 0
        if self.are_predators:
            for b in self.get_neighbors():
                if b.predator_weight == 0: # if is a predator
                    predator_vector = predator_vector + Vector.from_2_points(b.shape.location, self.shape.location)
                    num_preds += 1
        return predator_vector / num_preds * self.predator_weight if num_preds > 0 else predator_vector


    def update_motion_vector(self):
        self.motion_vector = self.motion_vector + self.cohesion() + self.alignment() + \
                             self.separation() + self.avoid_walls() + self.predators()
        if self.motion_vector.magnitude() > self.max_velocity:
            self.motion_vector.resize(self.max_velocity)

    def tick(self, dt):
        self.update_motion_vector()
        a, b, c = self.motion_vector.get_angle()
        self.shape.moveTo(*(self.motion_vector * dt + self.shape.location), 0, b, 90+c)


class Predator(Boid):
    predator_weight = 0
    color = RED

    def __init__(self):
        super(Predator, self).__init__()
        self.are_predators = True


class Frame(Window):
    num_boids = 50
    num_preds = 0
    planar = False

    def __init__(self):
        super(Frame, self).__init__()
        for i in range(self.num_boids):
            Boid()
        for p in range(self.num_preds):
            Predator()
        self.speed = 40


    def periodic(self, dt: float):
        super(Frame, self).periodic(dt)
        for b in Boid.all_boids:
            b.tick(dt)


if __name__ == '__main__':
    f = Frame()
    f.lock_mouse()
    f.set_fullscreen()
    f.start()