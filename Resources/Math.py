from math import *  # just steal standard library


class Vector(list):
    def __init__(self, *args):
        args = self._unpack_args(args)
        super(Vector, self).__init__(args)

    @staticmethod
    def _unpack_args(args):
        inner = type(args[0])
        return args[0] if inner == list or inner == tuple else args

    def __add__(self, other):
        return Vector([n1 + n2 for n1, n2 in zip(self, other)])

    def __sub__(self, other):
        return Vector([n1 - n2 for n1, n2 in zip(self, other)])

    def __mul__(self, other):
        return Vector(*[i*other for i in self])

    def __truediv__(self, other):
        return self * (1/other)

    def dot_product(self, other):
        return (self * other) / (self.magnitude() * other.magnitude())

    def __pow__(self, power, modulo=None):
        return self.dot_product(power)

    def magnitude(self):
        return sqrt(sum([i * i for i in self]))

    def unit_vector(self):
        x = 1/self.magnitude()
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
            x, y = self
            return degrees(acos(x)) if y >= 0 else 360-degrees(acos(x))
        elif dimension == 3:
            x, y, z = self
            xy = degrees(acos(x)) if y >= 0 else 360-degrees(acos(x))  # roll
            xz = degrees(acos(x)) if z >= 0 else 360-degrees(acos(x))  # yaw
            yz = degrees(acos(y)) if z >= 0 else 360-degrees(acos(y))  # pitch
            return xy, xz, yz

    @staticmethod
    def from_angles_and_mag(angles, mag: float):
        if type(angles) != list:
            angles = [angles]
        if len(angles) == 1:
            theta = angles[0]
            return Vector(cos(theta), sin(theta))
        else:
            pass

    def angle_to(self, other):
        return degrees(acos(self.dot_product(other)))

    def __repr__(self):
        return f"Vector{tuple(self)}"


class Matrix(list):
    def __init__(self, *args):
        args = self._unpack_args(args)
        self.dimension = len(args), len(args[0])
        # print(args)
        # print(self.dimension)
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
    # print([[(i2-i1)**2] for i1, i2 in zip(pos1, pos2)])
    return sqrt(sum([(i2-i1)**2 for i1, i2 in zip(pos1, pos2)]))
