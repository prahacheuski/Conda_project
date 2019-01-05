from pprint import pprint as pp
import struct


class Vector(object):
    __slots__ = '__x', '__y', '__z'

    def __init__(self, x, y, z):
        self.__x = x
        self.__y = y
        self.__z = z

    def __repr__(self):
        return f'Vector(x={self.__x}, y={self.__y}, z={self.__z})'


class Color(object):
    __slots__ = '__red', '__green', '__blue'

    def __init__(self, red, green, blue):
        self.__red = red
        self.__green = green
        self.__blue = blue

    def __repr__(self):
        return f'Color(red={self.__red}, green={self.__green}, blue={self.__blue})'


class Vertex(object):
    __slots__ = '__vector', '__color'

    def __init__(self, vector, color):
        self.__vector = vector
        self.__color = color

    def __repr__(self):
        return 'Vertex({!r}, {!r})'.format(self.__vector, self.__color)


def make_colored_vertex(x, y, z, red, green, blue):
    return Vertex(Vector(x, y, z), Color(red, green, blue))


if __name__ == '__main__':
    with open('colors.bin', 'rb') as f:
        buffer = f.read()

    vertices: list = []

    for fields in struct.iter_unpack('@3f3Hxx', buffer):
        vertex = make_colored_vertex(*fields)
        vertices.append(vertex)

    pp(vertices)
