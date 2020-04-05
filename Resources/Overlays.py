import pyglet
from pyglet.gl import *


class _TemplateOverlay:
    _mode = "c4B"

    def raw(self, vertices: list = [(0, 0)]):
        pass

    def lower_level(self, vertices):
        return self._mode, self.raw(vertices)

    def low_level(self, element):
        return self.lower_level(element.vertices)

    def get_group(self):
        return None


class Color(_TemplateOverlay):
    previously_made = []

    def __init__(self, x: int, y: int, z: int, alpha=255, type="rgb"):
        self.opacity = alpha
        self.type = type
        self.val1 = x
        self.val2 = y
        self.val3 = z
        self.previously_made.append(self)

    def convertToRGB(color):
        if color.type == "bgr":
            color.val1, color.val2 = color.val2, color.val1

    def convertToBGR(color):
        if color.type == "rgb":
            color.val1, color.val2 = color.val2, color.val1

    def convertToHSV(color):
        pass

    def assert_RGB(self):
        if self.type != "rgb":
            self.convertToRGB()

    def low_level(self, element):
        return self._mode, self.raw([i for i in range(element.amount_of_vertices)])

    def raw(self, vertices: list = [(0, 0)]):
        count = len(vertices)
        self.assert_RGB()
        color_data = (self.val1, self.val2, self.val3, self.opacity) * count
        return color_data

    def mix(self, other, percentage: float = 0.5):
        my_percentage = 1 - percentage
        other.assert_RGB()
        self.assert_RGB()
        return Color(int(my_percentage*self.val1 + percentage*other.val1),
                     int(my_percentage*self.val2 + percentage*other.val2),
                     int(my_percentage*self.val3 + percentage*other.val3))


class Gradient(_TemplateOverlay):  # this is test - does not actually work
    def __init__(self, top_color: Color, bottom_color: Color, type: str = "vertical"):
        self.color1 = top_color
        self.color2 = bottom_color
        self.type = type

    def _get_index(self):
        return 0 if self.type[0] == "h" else 1 if self.type[0] == "v" else None

    def raw(self, vertices: list = [(0, 0)]):
        index = self._get_index()
        data = ()
        _max = max(vertices, key=lambda i: i[index])[index]
        _min = min(vertices, key=lambda i: i[index])[index]
        if index == 0:  # if horizontal
            _max, _min = _min, _max  # flip to make left color1
        dif = _max - _min
        for pt in vertices:
            val = pt[index]
            val -= _min
            percentage = val / dif if dif != 0 else 0.5
            color_data = self.color2.mix(self.color1, percentage).raw()
            data += color_data
        return data


def tex_coord(x, y, n=4):
    """ Return the bounding vertices of the texture square.
    """
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m


def tex_coords(top, bottom, side):
    """ Return a list of the texture squares for the top, bottom and side.
    """
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side = tex_coord(*side)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side * 4)
    return result


class Texture(_TemplateOverlay):
    _mode = "t2f"

    def __init__(self, image_path: str, rect: tuple = (0, 0, 1, 1)):
        self.image = pyglet.image.load(image_path)
        self._texture = self.image.get_texture()
        x, y, w, h = rect
        self._coords = [x,y, x+w,y, x+w,y+h, x,y+h]
        # image_width, image_height = self.image.width, self.image.height
        self._data = self.image.get_image_data()
        self.TextureGroup = pyglet.graphics.TextureGroup(self._texture)
        # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, (image_width), (image_height), 0, GL_RGBA, GL_UNSIGNED_BYTE, data)

    def raw(self, vertices: list = None):
        # dimension = len(vertices[0])
        count = 4 if vertices is None else len(vertices)
        length = count//4
        return self._coords * length

    def get_group(self):
        return self.TextureGroup


class MultiTexture(_TemplateOverlay):
    _mode = "t2f"
    def __init__(self, bottom: Texture, top: Texture, front: Texture, back: Texture, right: Texture, left: Texture):
        self.bottom = bottom
        self.top = top
        self.front = front
        self.back = back
        self.right = right
        self.left = left

    def get_group(self):
        return self.bottom.get_group()

    def raw(self, vertices: list = [(0, 0)]):
        dimension = len(vertices[0])
        assert dimension == 3
        return self.bottom.raw([1, 1, 1, 1]) + self.top.raw([1, 1, 1, 1]) + self.front.raw([1, 1, 1, 1]) + \
               self.back.raw([1, 1, 1, 1]) + self.right.raw([1, 1, 1, 1]) + self.left.raw([1, 1, 1, 1])


# constants
RED = Color(255, 0, 0)
LIGHT_RED = Color(255, 50, 50)
YELLOW = Color(255, 255, 0)
BLACK = Color(0, 0, 0)
BLUE = Color(0, 0, 255)
LIGHT_BROWN = Color(165, 42, 42)
WHITE = Color(255, 255, 255)
GREY = Color(100, 100, 100)
LIGHT_GREY = Color(150, 150, 150)
OCEAN_BLUE = Color(0, 0, 155)
LIME_GREEN = Color(127, 255, 0)
GREEN = Color(0, 255, 0)
DARK_GREEN = Color(0, 100, 0)
PINK = Color(255, 192, 203)
ORANGE = Color(255, 69, 0)
BROWN = Color(165, 42, 42)
LIGHT_BLUE = Color(135, 206, 235)
