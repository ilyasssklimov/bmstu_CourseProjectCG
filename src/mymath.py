from math import pi, sin, cos, sqrt


class Vector:
    def __init__(self, start, finish):
        self.x = finish.x - start.x
        self.y = finish.y - start.y
        self.z = finish.z - start.z

    def __str__(self):
        return f'Vector({self.x}, {self.y}, {self.z})'

    def __neg__(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        return self

    def negative(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z

    def get_vector(self):
        return [self.x, self.y, self.z]

    def normalize(self):
        d = sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        self.x /= d
        self.y /= d
        self.z /= d

    def get_length_xy(self):
        return sqrt(self.x ** 2 + self.y ** 2)
    '''
    def get_normal(self):  # , start_2, finish_2):
        if self.x:
            normal = Vector(Point(1, 0, 0), Point(-self.y / self.x, 1, 0))
        else:
            normal = Vector(Point(0, 0, 0), Point(1, 0, 0))

        # if scalar_multiplication(normal, -Vector(start_2, finish_2)) < 0:
        #     normal.negative()

        return normal
    '''


class Angle:
    def __init__(self):
        self.angle = 0
        self.sin = 0
        self.cos = 1

    def set_angle(self, angle):
        self.angle = angle

    def set_sin(self, sin_angle):
        self.sin = sin_angle

    def set_cos(self, cos_angle):
        self.cos = cos_angle


def radians(angle):
    return angle * pi / 180


def degrees(angle):
    return angle * 180 / pi


def sin_deg(angle):
    return sin(radians(angle))


def cos_deg(angle):
    return cos(radians(angle))


def sign(num):
    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0


def add_repeats(points_1, points_2):
    p_1, p_2 = set(points_1), set(points_2)
    general = p_1 & p_2
    result = list(p_1 | p_2 - general) + list(general)

    return result


def find_by_key(d, key):
    key = sorted(list(key))
    for k in d:
        if sorted(list(k)) == key:
            return k
    raise KeyError('There is no such key in dictionary')


def find_y_min_max(vertices):
    if isinstance(vertices, list):
        cur_vertices = vertices
    elif isinstance(vertices, dict):
        cur_vertices = vertices.values()
    else:
        raise ValueError('Vertices should be list or dict')

    y_list = [vertex.y for vertex in cur_vertices]
    y_min, y_max = min(y_list), max(y_list)

    return y_min, y_max


def get_vertices_by_pairs(vertices_pairs):
    vertices = [*vertices_pairs[0]]
    del vertices_pairs[0]
    i = 1
    while vertices_pairs:
        for j in range(0, len(vertices_pairs)):
            if vertices[i] == vertices_pairs[j][0]:
                vertices.append(vertices_pairs[j][1])
                i += 1
                del vertices_pairs[j]
                break
            elif vertices[i] == vertices_pairs[j][1]:
                vertices.append(vertices_pairs[j][0])
                i += 1
                del vertices_pairs[j]
                break
    return vertices


def replace_list(src_list, old, new):
    new_iter = iter(new)
    return [x if x not in old else next(new_iter) for x in src_list]


def reverse_replace_list(src_list, old, new, const):
    new_list = replace_list(src_list, old, new)
    indices = [i for i in range(len(src_list))]
    indices.remove(src_list.index(const))
    new_list[indices[0]], new_list[indices[-1]] = new_list[indices[-1]], new_list[indices[0]]

    return new_list
