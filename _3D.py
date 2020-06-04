import pyglet
from Low_Level import LowLevel
from Resources.Overlays import WHITE, _TemplateOverlay
from Resources.Rendering import _ElementTemplate
from Resources.Math import Vector, distance, Matrix, rotate_3d
from math import *
from copy import deepcopy


class Template3d(_ElementTemplate):
    dimension = 3
    _vertex_type_base = "v3f"

    def __init__(self, overlay):
        super(Template3d, self).__init__(overlay)
        self.rotation = 0, 0, 0

    def _initialize(self):
        super(Template3d, self)._initialize()
        self._switch_coordinate_system()

    def moveTo(self, x: float = None, y: float = None, z: float = None,
               pitch: float = None, yaw: float = None, roll: float = None):
        cx, cy, cz = self.location
        dx = 0 if x is None else x - cx
        dy = 0 if y is None else y - cy
        dz = 0 if z is None else z - cz

        p, ya, r = self.rotation
        dp = 0 if pitch is None else pitch - p
        dya = 0 if yaw is None else yaw - ya
        dr = 0 if roll is None else roll - r
        self.move(dx, dy, dz, dp, dya, dr)

    def move(self, dx: float = 0.0, dy: float = 0.0, dz: float = 0.0,
             pitch: float = 0.0, yaw: float = 0.0, roll: float = 0.0):
        change = False
        if dx != 0 or dy != 0 or dz != 0:
            change = True
            x, y, z = self.location
            self.location = Vector(x+dx, y+dy, z+dz)
            dx = -dx
            self.vertices = [(x+dx, y+dy, z+dz) for x, y, z in self.vertices]
        if pitch != 0 or yaw != 0 or roll != 0:
            change = True
            self._rotate(pitch, yaw, roll)
        if change:
            self.update()

    def _rotate(self, pitch, yaw, roll):
        p, y, r = self.rotation
        self.rotation = p+pitch, y+yaw, r+roll
        self.vertices = rotate_3d(self.vertices, self._find_center(), pitch, yaw, roll)

    def _switch_coordinate_system(self):
        x, y, z = self.location
        self.location = -x, y, z


class Figure(Template3d):  # basic 3d thing
    mode = pyglet.graphics.GL_POLYGON


class LowerDimensional(Figure):  # putting stuff in _2d into 3d space
    function_class = type(distance)
    my_dir = None

    def __init__(self, lower: _ElementTemplate):
        self.my_dir = dir(LowerDimensional) if self.my_dir is None else self.my_dir  # keep all the 3d class variables
        attributes = self.get_attributes(lower)
        super(LowerDimensional, self).__init__(lower.overlay)
        for name, attribute in attributes:
            setattr(self, name, attribute)
        self.location = self._find_center()
        self.rotation = 0, lower.rotation, 0
        self._vertex_type = self._vertex_type_base
        self._initialize()
        lower.hide()
        del lower

    def get_attributes(self, lower):
        a = []
        lower_attr = dir(lower)
        for attribute_name in lower_attr:
            attribute = getattr(lower, attribute_name)
            if type(attribute) != self.function_class and not hasattr(LowerDimensional, attribute_name):
                a.append((attribute_name, attribute))
        return a


# todo clean this up - also improve location
class RectPrism(Figure):
    mode = pyglet.graphics.GL_QUADS
    # top_indices = 0, 12
    # bottom_indices = 12, 24
    # front_indices = 24, 36
    # back_indices = 36, 48
    # right_indices = 48, 60
    # left_indices = 60, 72

    def __init__(self, pos: tuple, l: float, w: float, h: float, texture: _TemplateOverlay = WHITE, group=None):
        super(RectPrism, self).__init__(texture)
        pos = LowLevel.convert_pos(pos)
        self.location = pos
        self.length = l
        self.width = w
        self.height = h
        self.vertices = self._get_vertices()
        self._initialize()

    # def _create_vertex_list(self, verts: tuple, overlay: _TemplateOverlay):
    #     return pyglet.graphics.vertex_list(4, (self._vertex_type, verts), overlay.lower_level(self._raw_to_points(verts)))

    def _get_vertices(self):
        return self._get_top() + self._get_bottom() + self._get_front() + self._get_back() + self._get_right() + self._get_left()

    def _get_all_vertices(self):
        return self._get_bottom() + self._get_top() + self._get_front() + self._get_back() + self._get_right() + self._get_left()

    def _get_creation_info(self):
        x, y, z = self.location
        dx, dy, dz = self.width / 2, self.height / 2, self.length / 2
        return x, y, z, dx, dy, dz

    def _get_top(self):
        x, y, z, dx, dy, dz = self._get_creation_info()
        # tlb, tlf, trb, trf
        return x - dx, y + dy, z - dz, x - dx, y + dy, z + dz, x + dx, y + dy, z + dz, x + dx, y + dy, z - dz

    def _get_bottom(self):
        x, y, z, dx, dy, dz = self._get_creation_info()
        # blb, blf, brb, brf
        return x - dx, y - dy, z - dz, x + dx, y - dy, z - dz, x + dx, y - dy, z + dz, x - dx, y - dy, z + dz

    def _get_front(self):
        x, y, z, dx, dy, dz = self._get_creation_info()
        return x - dx, y - dy, z + dz, x + dx, y - dy, z + dz, x + dx, y + dy, z + dz, x - dx, y + dy, z + dz

    def _get_back(self):
        x, y, z, dx, dy, dz = self._get_creation_info()
        return x + dx, y - dy, z - dz, x - dx, y - dy, z - dz, x - dx, y + dy, z - dz, x + dx, y + dy, z - dz

    def _get_right(self):
        x, y, z, dx, dy, dz = self._get_creation_info()
        return x - dx, y - dy, z - dz, x - dx, y - dy, z + dz, x - dx, y + dy, z + dz, x - dx, y + dy, z - dz

    def _get_left(self):
        x, y, z, dx, dy, dz = self._get_creation_info()
        return x + dx, y - dy, z + dz, x + dx, y - dy, z - dz, x + dx, y + dy, z - dz, x + dx, y + dy, z + dz
    '''
    def set_top_texture(self, texture: _TemplateOverlay):
        self._top_texture = texture
        self.top = self._create_vertex_list(self._get_top(), self._top_texture)

    def set_bottom_texture(self, texture: _TemplateOverlay):
        self._bottom_texture = texture
        self.bottom = self._create_vertex_list(self._get_bottom(), self._bottom_texture)

    def set_front_texture(self, texture: _TemplateOverlay):
        self._front_texture = texture
        self.front = self._create_vertex_list(self._get_front(), self._front_texture)

    def set_back_texture(self, texture: _TemplateOverlay):
        self._back_texture = texture
        self.back = self._create_vertex_list(self._get_back(), self._back_texture)

    def set_right_texture(self, texture: _TemplateOverlay):
        self._right_texture = texture
        self.right = self._create_vertex_list(self._get_right(), self._right_texture)

    def set_left_texture(self, texture: _TemplateOverlay):
        self._left_texture = texture
        self.left = self._create_vertex_list(self._get_left(), self._left_texture)

    def _get_vertex_list(self):
        # self._establish_faces()
        return super(RectPrism, self)._get_vertex_list()  # self._establish_faces()

    def render(self):  # todo implent batch rendering here
        super(RectPrism, self).render()
        return
        self.top.draw(self.mode)
        self.bottom.draw(self.mode)
        self.front.draw(self.mode)
        self.back.draw(self.mode)
        self.left.draw(self.mode)
        self.right.draw(self.mode)
        
    '''

    def get_nearest_point(self, pt: tuple):
        x, y, z, dx, dy, dz = self._get_creation_info()
        x2, y2, z2 = pt
        x1 = x-dx if x2 <= x-dx else x2 if x2 < x+dx else x+dx
        y1 = y - dy if y2 <= y - dy else y2 if y2 < y + dy else y + dy
        z1 = z - dz if z2 <= z - dz else z2 if z2 < z + dz else z + dz
        return x1, y1, z1

    def distance(self, pt):
        if isinstance(pt, _ElementTemplate):
            pt = pt.get_nearest_point(self.location)
        x2, y2, z2 = pt
        x1, y1, z1 = self.get_nearest_point(pt)
        d = distance((x1, y1, z1), pt)
        return d if x1 != x2 or y1 != y2 or z1 != z2 else -1  # reverse if inside cube



class Cube(RectPrism):
    def __init__(self, pos: tuple, side_length: float, texture: _TemplateOverlay = WHITE):
        super(Cube, self).__init__(pos, side_length, side_length, side_length, texture)


class Sphere(Figure):
    mode = pyglet.gl.GL_TRIANGLES  # pyglet.gl.GL_TRIANGLE_STRIP
    unit_sphere = None
    detail = 4

    def __init__(self, pos: tuple, radius: float, overlay: _TemplateOverlay):
        if self.unit_sphere is None:
            self.unit_sphere = self.create_sphere()
        pos = LowLevel.convert_pos(pos)
        super(Sphere, self).__init__(overlay)
        self.location = pos
        self.radius = radius
        self.vertices = deepcopy(self.unit_sphere)
        for i, pt in enumerate(self.vertices):
            self.vertices[i] = pt * self.radius + pos
        # self.vertices = self._get_vertices()
        self._initialize()

    def _get_vertices(self, step):
        ox, oy, oz = self.location
        verts = []
        previous_layer = []
        for lat in range(-90, 90, step):
            is_first_layer = previous_layer == []
            current_layer = []
            stuff = []
            for i, lon in enumerate(range(-180, 181, step)):
                x = -cos(radians(lat)) * cos(radians(lon)) * self.radius
                y = sin(radians(lat)) * self.radius
                z = cos(radians(lat)) * sin(radians(lon)) * self.radius
                pos = x+ox, y+oy, z+oz
                current_layer.append(pos)
                if is_first_layer and i > 0 and False:
                    stuff.append(previous_layer[i])
                    stuff.append(previous_layer[i-1])
                x = -cos(radians((lat + step))) * cos(radians(lon)) * self.radius +0.1
                y = sin(radians((lat + step))) * self.radius + 0.1
                z = cos(radians((lat + step))) * sin(radians(lon)) * self.radius + 0.1
                pos = x + ox, y + oy, z + oz
                current_layer.append(pos)
                if is_first_layer and i > 0 and False:
                    stuff.append(previous_layer[i])
                    stuff.append(previous_layer[i - 1])
            previous_layer = current_layer
            if not is_first_layer:
                verts.extend(current_layer)
                verts.extend(stuff)
        return verts

    octahedron_vertices = [
        Vector([1.0, 0.0, 0.0]),  # 0
        Vector([-1.0, 0.0, 0.0]),  # 1
        Vector([0.0, 1.0, 0.0]),  # 2
        Vector([0.0, -1.0, 0.0]),  # 3
        Vector([0.0, 0.0, 1.0]),  # 4
        Vector([0.0, 0.0, -1.0])  # 5
    ]
    octahedron_triangles = [
        [octahedron_vertices[0], octahedron_vertices[4], octahedron_vertices[2]],
        [octahedron_vertices[2], octahedron_vertices[4], octahedron_vertices[1]],
        [octahedron_vertices[1], octahedron_vertices[4], octahedron_vertices[3]],
        [octahedron_vertices[3], octahedron_vertices[4], octahedron_vertices[0]],
        [octahedron_vertices[0], octahedron_vertices[2], octahedron_vertices[5]],
        [octahedron_vertices[2], octahedron_vertices[1], octahedron_vertices[5]],
        [octahedron_vertices[1], octahedron_vertices[3], octahedron_vertices[5]],
        [octahedron_vertices[3], octahedron_vertices[0], octahedron_vertices[5]]
    ]
    
    def divide_triangle(self, triangle, depth):
        if depth <= 0:
            return [triangle]
        vert1, vert2, vert3 = triangle
        a = (vert1 + vert2) / 2
        b = (vert2 + vert3) / 2
        c = (vert1 + vert3) / 2
        triangle1 = vert1, a, c
        triangle2 = vert2, a, b
        triangle3 = vert3, b, c
        triangle4 = a, b, c
        triangles = []
        triangles.extend(self.divide_triangle(triangle1, depth-1))
        triangles.extend(self.divide_triangle(triangle2, depth-1))
        triangles.extend(self.divide_triangle(triangle3, depth-1))
        triangles.extend(self.divide_triangle(triangle4, depth-1))
        return triangles
    
    def inflate(self, triangles):
        points = []
        for triangle in triangles:
            for vector in triangle:
                points.append(vector.unit_vector())
        return points

    def create_sphere(self):
        recurision_level = self.detail
        triangles = []
        for triangle in self.octahedron_triangles:
            triangles.extend(self.divide_triangle(triangle, recurision_level))
        return self.inflate(triangles)

    def get_nearest_point(self, pt):
        v = Vector.from_2_points(self.location, pt)
        v.resize(self.radius)
        return v + self.location

    def distance(self, pt: tuple):
        return super(Sphere, self).distance(pt) - self.radius


class Combination(_ElementTemplate):
    def __init__(self, *args):
        self.vertices = []

    def _get_vertex_data(self, vertices: tuple, overlay: _TemplateOverlay):
        pass


class Mesh:
    pass

