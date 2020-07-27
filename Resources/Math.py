from math import *  # just steal standard library


class Vector(list):
    def __init__(self, *args):
        args = self._unpack_args(args)
        super(Vector, self).__init__(args)

    @staticmethod
    def _unpack_args(args):
        inner = type(args[0])
        return args[0] if inner == list or inner == tuple or inner == Vector else args

    def _empty(self):
        while len(self) > 0:
            self.pop()

    def __add__(self, other):
        return Vector([n1 + n2 for n1, n2 in zip(self, other)])

    def __sub__(self, other):
        return Vector([n1 - n2 for n1, n2 in zip(self, other)])

    def __mul__(self, other):
        if type(other) == Vector:
            return self.cross_product(other)
        return Vector(*[i*other for i in self])

    def __truediv__(self, other):
        return self * (1/other)

    def dot_product(self, other):
        return sum([n1 * n2 for n1, n2 in zip(self, other)])

    def cross_product(self, other):
        pass

    def __pow__(self, power, modulo=None):
        return self.dot_product(power)

    def magnitude(self):
        return sqrt(sum([i * i for i in self]))

    def unit_vector(self):
        x = 1/self.magnitude() if self.magnitude() != 0 else Vector(0, 1, 0)
        return self * x

    def resize(self, new_len):
        x = new_len/self.magnitude()
        for i in range(len(self)):
            self[i] *= x

    @staticmethod
    def from_2_points(pos1, pos2):
        vals = [i2 - i1 for i1, i2 in zip(pos1, pos2)]
        return Vector(*vals)

    def get_angle(self):
        dimension = len(self)
        if dimension == 2:
            x, y = self.unit_vector()
            return degrees(acos(x)) if y >= 0 else 360-degrees(acos(x))
        elif dimension == 3:
            x, y, z = self.unit_vector()
            xy = degrees(acos(x/sqrt(x*x+y*y))) if y >= 0 else 360-degrees(acos(x/sqrt(x*x+y*y)))  # roll
            xz = degrees(acos(x/sqrt(x*x+z*z))) if z >= 0 else 360-degrees(acos(x/sqrt(x*x+z*z)))  # yaw
            yz = degrees(acos(y/sqrt(z*z+y*y))) if z >= 0 else 360-degrees(acos(y/sqrt(z*z+y*y)))  # pitch
            return xy, xz, yz

    @staticmethod
    def from_angles_and_mag(angles, mag: float):
        if type(angles) != list:
            angles = [angles]
        if len(angles) == 1:
            theta = angles[0]
            return Vector(cos(theta), sin(theta)) * mag
        else:
            pass

    def angle_to(self, other):
        if self.magnitude() == 0 or other.magnitude() == 0:
            print(self, other)
        return degrees(acos(self.dot_product(other) / (self.magnitude() * other.magnitude())))

    def __repr__(self):
        return f"Vector{tuple(self)}"


class Matrix(list):
    def __init__(self, *args):
        args = self._unpack_args(args)
        self.dimension = len(args), len(args[0])
        super(Matrix, self).__init__(args)

    def _unpack_args(self, args):
        inner = type(args[0][0])
        if inner == list or inner == tuple:
            args = args[0]
        return [Vector(arg) for arg in args]

    def __mul__(self, other):
        result = self.zero_matrix(rows=len(self[0]), cols=len(other))
        # height of self
        for row1 in range(len(self[0])):
            # width of other
            for col2 in range(len(other)):
                # height of other
                for row2 in range(len(other[0])):
                    result[col2][row1] += self[row2][row1] * other[col2][row2]
        return result

    def __add__(self, other):
        new = []
        for row1, row2 in zip(self, other):
            new.append([i1 + i2 for i1, i2 in zip(row1, row2)])
        return Matrix(*new)

    def __sub__(self, other):
        new = []
        for row1, row2 in zip(self, other):
            new.append([i1 - i2 for i1, i2 in zip(row1, row2)])
        return Matrix(new)

    @staticmethod
    def zero_matrix(rows, cols=None):
        cols = rows if cols is None else cols
        return Matrix(*[[0 for i in range(rows)] for j in range(cols)])

    @staticmethod
    def identity_matrix(dimension):
        new = []
        for r in range(dimension):
            new_row = []
            for c in range(dimension):
                new_row.append(1 if r == c else 0)
            new.append(new_row)
        return Matrix(*new)


def distance(pos1, pos2):
    return sqrt(sum([(i2-i1)**2 for i1, i2 in zip(pos1, pos2)]))


def rotate_polygon(list_of_points, rotation, center):
    center_x, center_y = center
    x_cordinates = []
    y_cordinates = []

    for x, y in list_of_points:
        x_cordinates.append(x-center_x)
        y_cordinates.append(y-center_y)
    point_matrix = []
    point_matrix.append(x_cordinates)
    point_matrix.append(y_cordinates)

    rotation = radians(rotation)
    rotation_matrix = [
        [cos(rotation), -sin(rotation)],
        [sin(rotation), cos(rotation)]
    ]

    result = [[], []]
    for i in range(len(x_cordinates)):  # result = R * thing1
        result[0].append(0)
        result[1].append(0)
    for i in range(len(rotation_matrix)):
        # iterate through columns of Y
        for j in range(len(point_matrix[0])):
            # iterate through rows of Y
            for k in range(len(point_matrix)):
                result[i][j] += rotation_matrix[i][k] * point_matrix[k][j]

    polygon = []
    for x, y in zip(result[0], result[1]):
        polygon.append((x + center_x, y + center_y))

    return polygon


def rotate_3d(list_of_points, center, pitch, yaw, roll):
    '''
    A rotation of points in 3d space around a central point
    :param list_of_points: all the points that are having the rotation applied
    :param center: center of rotation
    :param pitch: yz axis
    :param yaw: xy axis
    :param roll: xy axis
    :return: a list of where points are after the rotation
    '''
    dx, dy, dz = center
    translation_vector = Vector([dx, dy, dz])
    point_matrix = Matrix(list_of_points)
    for i, vector in enumerate(point_matrix):
        point_matrix[i] = vector - translation_vector
    x = radians(pitch)
    y = radians(yaw)
    z = radians(roll)
    rotation_matrix = Matrix(
        [cos(z) * cos(y), cos(y) * sin(x) * sin(z) - cos(x) * sin(y), cos(x) * cos(y) * sin(z) + sin(x) * sin(y)],
        [cos(z) * sin(y), cos(x) * cos(y) + sin(x) * sin(z) * sin(y), cos(x) * sin(z) * sin(y)-cos(y) * sin(x)],
        [-sin(z), cos(z) * sin(x), cos(x) * cos(z)]
    )
    rotated_matrix = rotation_matrix * point_matrix
    for i, vector in enumerate(rotated_matrix):
        rotated_matrix[i] = vector + translation_vector
    new_points = [tuple(vector) for vector in rotated_matrix]
    return new_points
