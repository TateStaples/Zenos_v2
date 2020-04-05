# import pyglet
from Zenos_package import *
from math import *
from time import time

# basic simulatoin of our solar system

def tick(dt):
    update(dt/slow_mo)
    # draw()


def update(dt):
    for planet in Planet.all_planets:
        planet.apply_all(dt)
    # set_conversion()
    for planet in Planet.all_planets:
        planet.move_(dt)


# def draw():
#     window.clear()
#     for planet in Planet.all_planets:
#         planet.draw()


def center(images):
    """Sets an image's anchor point to its center"""
    for image in images:
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2


def set_conversion():
    global current_conversion, unit_per_pixel, desired_width
    current_conversion = unit_per_pixel / desired_width


def mass_converter(x):
    return x / 2000000


def au_to_parsecs(*args):
    return [au * 4.84814e-6 for au in args]


def au_to_km(*args):
    return [au * 149597870.700 for au in args]


def au_per_day_to_kms(*args):
    return [au_to_km(apd)[0] / 86400.0 for apd in args]  # should be 3+7


class Frame(Window):
    def periodic(self, dt: float):
        super(Frame, self).periodic(dt)
        tick(dt)

    def on_key_press(self, symbol, modifiers):
        super(Frame, self).on_key_press(symbol, modifiers)
        global slow_mo, unit_per_pixel
        if symbol == self.keys.Z:
            slow_mo /= 2
        elif symbol == self.keys.X:
            slow_mo *= 2
        elif symbol == self.keys.C:
            unit_per_pixel -= .00001
            set_conversion()
        elif symbol == self.keys.V:
            unit_per_pixel += .00001
            set_conversion()
        elif symbol == pyglet.window.key.SPACE:
            for planet in Planet.all_planets:
                planet.x_vel *= -1
                planet.y_vel *= -1
                planet.z_vel *= -1

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.speed += scroll_y * 2


class Planet(ThreeD.Sphere):
    all_planets = []
    gravitation_constant = 4.302 * 10 ** -3  # 10000000000

    '''
    Units:
    distance: parsecs
    velocity: kilometers/second
    mass: solar_units
    time = years?
    '''

    def __init__(self, image, cords, mass, velocities=(0, 0, 0), image_dimensions=(50, 50)):
        self.x_vel, self.y_vel, self.z_vel = velocities
        self.mass = mass
        self.real_x, self.real_y, self.real_z = cords
        super(Planet, self).__init__(self.sim_pos(), 0.5, image)
        self.all_planets.append(self)

    @staticmethod
    def real_to_sim(pos):
        try:
            centered = Vector(pos) - Vector(Sun.real_x, Sun.real_y, Sun.real_z)
        except NameError:
            centered = Vector(pos)
        return centered / current_conversion

    def sim_pos(self):
        return self.real_to_sim((self.real_x, self.real_z, self.real_y))

    def apply_all(self, dt):
        for planet in self.all_planets:
            if planet is self:
                continue
            self.apply_planet(planet, dt)

    def apply_planet(self, other_planet, dt):
        x_force, y_force, z_force = self.get_force(other_planet)
        self.apply_force(x_force, y_force, z_force, dt)

    def apply_force(self, x, y, z, dt):
        self.x_vel += x / self.mass * dt
        self.y_vel += y / self.mass * dt
        self.z_vel += z / self.mass * dt
        # print(f"Force: x={x}, y={y}, z={z}")

    def get_force(self, other_planet):
        delta_x = self.real_x - other_planet.real_x
        delta_y = self.real_y - other_planet.real_y
        delta_z = self.real_z - other_planet.real_z
        dis = self.pathag([delta_x, delta_y, delta_z])
        mass1 = self.mass
        mass2 = other_planet.mass
        magnitude = (self.gravitation_constant * mass1 * mass2) / (dis ** 2)
        r_hat = delta_x / dis, delta_y / dis, delta_z / dis
        components = (-hat * magnitude for hat in r_hat)
        return components

    def get_angle(self, other_planet):
        delta_x = self.real_x - other_planet.real_x
        delta_y = self.real_y - other_planet.real_y
        delta_z = self.real_z = other_planet.real_z
        if delta_y == 0:
            xy_angle = pi / 2 if delta_x > 0 else 3 * pi / 2
        else:
            xy_angle = atan(delta_x / delta_y)
            if delta_y > 0:
                xy_angle += pi
        if delta_z == 0:
            xz_angle = pi / 2 if delta_x > 0 else 3 * pi / 2
        else:
            xz_angle = atan(delta_x / delta_z)
            if delta_z > 0:
                xz_angle += pi
        return xy_angle, xz_angle  # note this is in radian

    def get_screen_pos(self):
        # todo change view angle
        try:
            x1, y1 = self.real_x - Sun.real_x, self.real_y - Sun.real_y  # keeps the screen centered on the Sun
        except NameError:
            x1, y1 = self.real_x, self.real_y
        x2, y2 = x1 / current_conversion, y1 / current_conversion
        # print(f"original x: {self.real_x}, streched: {x1}")
        return x2 + window.width / 2, y2 + window.height / 2

    def move_(self, dt):
        if self is Earth and self.real_y < 0 and self.real_y + self.y_vel * dt > 0:
            global years_passed, start_time
            years_passed += 1
            print(f"{years_passed} years have passed, {time() - start_time}")
            start_time = time()
        self.real_x += self.x_vel * dt
        self.real_y += self.y_vel * dt
        self.real_z += self.z_vel * dt
        self.x, self.y = self.get_screen_pos()
        self.moveTo(*(self.sim_pos()))

    @staticmethod
    def pathag(vals):
        sum = 0
        for i in vals:
            sum += i ** 2
        return sqrt(sum)


if __name__ == '__main__':
    window = Frame()
    window.set_fullscreen()
    start_time = time()
    unit_per_pixel = 0.0001456762698498
    desired_width = 300
    seconds_per_year = 100
    slow_mo = 952380.95 * seconds_per_year
    years_passed = 0
    current_conversion = unit_per_pixel / desired_width
    Sun = Planet(
        image=YELLOW,
        image_dimensions=(20, 20),
        cords=(0, 0, 0),
        velocities=(0, 0, 0),
        mass=1  # in solar mass
    )
    X = 6.711820340656954E-02
    Y = -4.433097504115295E-01
    Z = -4.334619357941907E-02
    VX = 2.213358745453331E-02
    VY = 5.861224535918585E-03
    VZ = -1.551747830294273E-03
    Mercury = Planet(
        image=GREY,
        image_dimensions=(5, 5),
        cords=au_to_parsecs(X, Y, Z),
        velocities=au_per_day_to_kms(VX, VY, VZ),
        mass=mass_converter(0.330)  # in solar mass
    )
    X = -6.665252078700974E-01
    Y = 2.845663634115694E-01
    Z = 4.204916311133774E-02
    VX = -7.916132290777207E-03
    VY = -1.875201797693838E-02
    VZ = 1.993049500413981E-04

    Venus = Planet(
        image=ORANGE,
        image_dimensions=(5, 5),
        cords=au_to_parsecs(X, Y, Z),
        velocities=au_per_day_to_kms(VX, VY, VZ),
        mass=mass_converter(4.87)  # in solar mass
    )
    X = -9.732168588388307E-01
    Y = -2.417364230098931E-01
    Z = 5.665555127262041E-05
    VX = 3.997870385508543E-03
    VY = -1.672498143967054E-02
    VZ = 5.507834514499402E-07
    Earth = Planet(
        image=GREEN,
        image_dimensions=(5, 5),
        cords=au_to_parsecs(X, Y, Z),
        velocities=au_per_day_to_kms(VX, VY, VZ),
        mass=mass_converter(5.97)  # in solar mass
    )
    X = -1.986014492336561E-01
    Y = -1.451514904821706E+00
    Z = -2.576069414069500E-02
    VX = 1.439197798526096E-02
    VY = -6.448013295978382E-04
    VZ = -3.665143740675675E-04
    Mars = Planet(
        image=RED,
        image_dimensions=(5, 5),
        cords=au_to_parsecs(X, Y, Z),
        velocities=au_per_day_to_kms(VX, VY, VZ),
        mass=mass_converter(0.642)  # in solar mass
    )
    X = 1.212472675407543E+00
    Y = -5.041284978683700E+00
    Z = -6.216532977670807E-03
    VX = 7.243818799918126E-03
    VY = 2.123610312064836E-03
    VZ = -1.708863890806112E-04
    Jupiter = Planet(
        image=BROWN,
        image_dimensions=(5, 5),
        cords=au_to_parsecs(X, Y, Z),
        velocities=au_per_day_to_kms(VX, VY, VZ),
        mass=mass_converter(1898)  # in solar mass
    )
    X = 4.244677118083809E+00
    Y = -9.071790386481778E+00
    Z = -1.124123839657324E-02
    VX = 4.744027180212408E-03
    VY = 2.349037731208436E-03
    VZ = -2.299837026736019E-04
    Saturn = Planet(
        image=PINK,
        image_dimensions=(5, 5),
        cords=au_to_parsecs(X, Y, Z),
        velocities=au_per_day_to_kms(VX, VY, VZ),
        mass=mass_converter(568)  # in solar mass
    )
    X = 1.600385881408165E+01
    Y = 1.166992045140301E+01
    Z = -1.639895383616876E-01
    VX = -2.346178103904706E-03
    VY = 2.994646572134732E-03
    VZ = 4.156423978886388E-05
    Uranus = Planet(
        image=BLUE,
        image_dimensions=(5, 5),
        cords=au_to_parsecs(X, Y, Z),
        velocities=au_per_day_to_kms(VX, VY, VZ),
        mass=mass_converter(86.8)  # in solar mass
    )
    X = 2.929834268043162E+01
    Y = -6.069354488358040E+00
    Z = -5.502230307240934E-01
    VX = 6.157760589569711E-04
    VY = 3.092089587798861E-03
    VZ = -7.813901375734837E-05
    Neptune = Planet(
        image=LIGHT_BLUE,
        image_dimensions=(5, 5),
        cords=au_to_parsecs(X, Y, Z),
        velocities=au_per_day_to_kms(VX, VY, VZ),
        mass=mass_converter(102)  # in solar mass
    )
    window.lock_mouse()
    window.start()
