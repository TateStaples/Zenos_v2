import pyglet
from Resources.Overlays import _TemplateOverlay
from Resources.Math import distance, Vector, cos, radians
from copy import deepcopy

low = None


def multidimensional_rotation(list_of_points, center, **kwargs):
    variable_translator = {'x': 1, 'y': 2, 'z': 3, 'w': 4}  # variable to dimension of significance
    dimension = len(list_of_points[0])
    coords = [[] for i in range(dimension)]
    # position matrix
    for pt in list_of_points:
        for i, num in enumerate(pt):
            coords[i] = num

    # rotation matricies
    # rotations = [radians(arg) for arg in kwargs]

    # multiply the rotation matricies

    # multiply postion * rotation

    # translate back


class _ElementTemplate:
    mode = None
    dimension = None
    _indexed = True
    _vertex_type_base = ""
    default_group = None

    def __init__(self, overlay: _TemplateOverlay):
        self.overlay = overlay
        self.vertices = None
        self.vertex_list = None
        self._raw_points = None
        self.group = self.default_group
        self.settings = None  # can be a pyglet Group
        self.location = None
        self.amount_of_vertices = None
        self.showing = True
        self._vertex_type = self._vertex_type_base
        self.rotation = None

    def _initialize(self):
        if type(self.vertices[0]) == float:
            self._raw_points = tuple(self.vertices)
            self.vertices = self._raw_to_points(self._raw_points)
        else:
            self._raw_points = self._points_to_raw(self.vertices)
        self.amount_of_vertices = len(self._raw_points) // self.dimension
        self.vertex_list = self.group.add_raw(*self._get_vertex_data(self._raw_points, self.overlay))

    def render(self):
        self.vertex_list.draw(self.mode)

    def update(self):
        self._raw_points = self._points_to_raw(self.vertices)
        self.vertex_list.vertices = list(self._raw_points)

    def set_overlay(self, overlay: _TemplateOverlay):
        self.overlay = overlay
        self.vertex_list = self._get_vertex_list()

    def moveTo(self):  # override in other templates
        pass

    def move(self):  # override in other templates
        pass

    def _get_vertex_data(self, vertices: tuple, overlay: _TemplateOverlay):
        count = len(vertices) // self.dimension
        return count, self.mode, Grupa_Groups(overlay.get_group(), self.settings), tuple([i for i in range(count)]), \
               (self._vertex_type, vertices), overlay.low_level(self)

    def vert_data(self):
        return self._get_vertex_data(self._raw_points, self.overlay)

    @staticmethod
    def _points_to_raw(points: list):
        x = []
        for pt in points:
            x += pt
        return tuple(x)

    def _raw_to_points(self, raw_points: tuple):
        stuff = []
        raw_points = list(raw_points)
        while len(raw_points) > 0:
            stuff.append(tuple(raw_points[0:self.dimension]))
            raw_points = raw_points[self.dimension: len(raw_points)]
        return stuff

    def _get_vertex_list(self):
        return self._make_vertex_list(self._raw_points, self.overlay)

    def _make_vertex_list(self, vertices: tuple, overlay: _TemplateOverlay):
        return self.group.add_raw(*self._get_vertex_data(vertices, overlay)) if self.group is not None else pyglet.graphics.vertex_list(self.amount_of_vertices, (self._vertex_type, self._raw_points), self.overlay.low_level(self))

    def pair(self, other):  # can't type while in the class
        other.group.add(self)

    def unpair(self, other):
        self.group.remove(other)

    def __add__(self, other):
        self.pair(other)

    def __sub__(self, other):
        self.unpair(other)

    def hide(self):
        if self.showing:
            self.showing = False
            self.group.remove(self)
            self.vertex_list = self._get_vertex_list()

    def show(self):
        if not self.showing:
            self.showing = True
            self.vertex_list.delete()
            self.vertex_list = self.default_group.add(self)

    def __del__(self):
        if hasattr(self, "vertex_list") and self.vertex_list is not None:
            self.vertex_list.delete()

    def get_nearest_point(self, pt):
        return self.location

    def distance(self, other):
        if isinstance(other, _ElementTemplate):
            p1 = self.get_nearest_point(other.location)
            p2 = other.get_nearest_point(self.location)
        else:
            p1 = self.get_nearest_point(other)
            p2 = other
        return distance(p1, p2)

    def _find_center(self):
        sums = [0 for i in range(self.dimension)]
        for pt in self.vertices:
            for dimension, value in enumerate(pt):
                sums[dimension] += value
        count = len(self.vertices)
        return tuple([dimension_sum / count for dimension_sum in sums])

    def resize(self, amount):
        self.vertices = [tuple([(vertex[i] - self.location[i]) * amount + self.location[i] for i in range(len(vertex))]) for vertex in self.vertices]
        self.update()

    def __mul__(self, other):
        self.resize(other)

    def put_on_top(self):
        g = self.group
        g - self
        self.vertex_list = g + self

    def copy(self, pos=None):
        c = deepcopy(self)
        if pos is not None:
            c.moveTo(*pos)
        return c

    def __repr__(self):
        return f"{type(self).__name__} @ {self.location}"


# draw group  # todo make this better
class Group:
    def __init__(self, *args):
        self.type = None
        self.Batch3 = pyglet.graphics.Batch()
        self.Batch2 = pyglet.graphics.Batch()
        self.Batch4 = None
        self._2 = 0
        self._3 = 0
        for item in args:
            self.add(item)

    def render(self):
        if self._3 > 0:
            low.enable_3d()
            self.Batch3.draw()
        if self._2 > 0:
            low.assert_2d()
            self.Batch2.draw()

    def add_raw(self, count: int, mode, group: pyglet.graphics.Group, indices: list, position_data: tuple, overlay_data: tuple):
        dimension = int(position_data[0][1])
        if dimension == 2:
            self._2 += 1
            return self.Batch2.add_indexed(count, mode, group, indices, position_data, overlay_data)
            # count, mode, group, indices, data
        elif dimension == 3:
            self._3 += 1
            return self.Batch3.add_indexed(count, mode, group, indices, position_data, overlay_data)
        else:
            pass

    def add(self, other: _ElementTemplate):
        if other.group is None:
            other.group = self
            return self.add_raw(*other.vert_data())
        vertex_list = other.vertex_list
        if other.dimension == 2:
            other_batch = other.group.Batch2
            other_batch.migrate(vertex_list, other.mode, other.overlay.get_group(), self.Batch2)  # vertex list, mode, group, batch
            self._2 += 1
        elif other.dimension == 3:
            other_batch = other.group.Batch3
            other_batch.migrate(vertex_list, other.mode, other.overlay.get_group(), self.Batch3)  # vertex list, mode, group, batch
            self._3 += 1
        else:
            pass
        other.group = self
        return vertex_list

    def remove(self, other: _ElementTemplate):
        other.group = None
        other.vertex_list.delete()
        if other.dimension == 2:
            self._2 -= 1
        elif other.dimension == 3:
            self._3 -= 1
        else:
            pass

    def __add__(self, other: _ElementTemplate):
        return self.add(other)

    def __sub__(self, other: _ElementTemplate):
        return self.remove(other)


class Grupa_Groups(pyglet.graphics.Group):
    def __new__(cls, *args, **kwargs):
        args = list(filter(lambda x: x is not None, args))
        if len(args) == 0:
            return None
        if len(args) == 1:
            return args[0]
        return super(Grupa_Groups, cls).__new__(cls)

    def __init__(self, *args):
        super(Grupa_Groups, self).__init__()
        self.groups = args

    def set_state(self):
        for group in self.groups:
            group.set_state()

    def set_state_recursive(self):
        for group in self.groups:
            group.set_state_recursive()

    def unset_state(self):
        for group in self.groups:
            group.unset_state()

    def unset_state_recursive(self):
        for group in self.groups:
            group.unset_state_recursive()


class WeirdRender(pyglet.graphics.Group):
    parent = None

    def unset_state(self):
        pyglet.gl.glEnableClientState(pyglet.graphics.GL_NV_primitive_restart)
        # pyglet.gl.glEnable(pyglet.gl.GL_PRIMITIVE_RESTART)


_ElementTemplate.default_group = Group()