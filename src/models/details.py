from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush
import src.general.config as config
from copy import deepcopy
from src.utils.point import divide_line_by_num
from src.utils.matrix import MatrixPlane
from src.utils.mymath import find_by_key, get_vertices_by_pairs, replace_list, reverse_replace_list, get_plane_cosine
from src.utils.mymath import Vector
from src.utils.point import Point


# TODO: наследовать детали от одного класса (возможно)
# TODO: убрать дублирование кода, рефакторинг!


class Detail:
    def __init__(self, vertices, edges, offset, name, model_name, eccentric=True):
        if model_name == config.CUBE:
            self.cfg = config.CubeConfig()
        elif model_name == config.PYRAMID:
            self.cfg = config.PyramidConfig()
        else:
            raise ValueError('Invalid model name param')

        self.vertices = vertices
        self.edges = edges
        self.name = None
        self.prev_name = None
        self.set_name(name)
        self.name_for_color = list(name)
        self.colors = self.cfg.get_center_colors()
        if eccentric:
            self.sides = self.cfg.get_eccentric_detail_sides()

        self.move(offset)
        self.move(config.Config().center)

    def __str__(self):
        result = 'Detail\n[\n'
        for vertex in self.vertices:
            result += f'    {vertex},\n'
        result += ']\n'
        return result

    def turn_ox(self, angle):
        for vertex in self.vertices.values():
            vertex.turn_ox(angle)

    def turn_oy(self, angle):
        for vertex in self.vertices.values():
            vertex.turn_oy(angle)

    def turn_oz(self, angle):
        for vertex in self.vertices.values():
            vertex.turn_oz(angle)

    def move(self, offset):
        for vertex in self.vertices.values():
            vertex.move(offset)

    def scale(self, k, point):
        for vertex in self.vertices.values():
            vertex.scale(k, point)

    def turn_ox_funcs(self, sin_angle, cos_angle):
        for vertex in self.vertices.values():
            vertex.turn_ox_funcs(sin_angle, cos_angle)

    def turn_oy_funcs(self, sin_angle, cos_angle):
        for vertex in self.vertices.values():
            vertex.turn_oy_funcs(sin_angle, cos_angle)

    def turn_oz_funcs(self, sin_angle, cos_angle):
        for vertex in self.vertices.values():
            vertex.turn_oz_funcs(sin_angle, cos_angle)

    def set_name(self, name):
        self.prev_name = self.name
        self.name = list(name)

    def update_sides(self, side, direction):
        exchange = self.cfg.get_exchanges_centers()[side]

        dir_range = range(len(exchange) - 2, -1, -1) if direction > 0 else range(1, len(exchange))
        saved_ind = -1 if direction > 0 else 0

        tmp = self.sides[exchange[saved_ind]]
        for i in dir_range:
            i_to = exchange[i + direction]
            i_from = exchange[i]
            self.sides[i_to] = self.sides[i_from]
        self.sides[exchange[saved_ind + direction]] = tmp

        set_name = set(self.name)
        set_prev_name = set(self.prev_name)
        old_letter = list(set_prev_name - set_name)
        new_letter = list(set_name - set_prev_name)

        if len(self.name) == 2:
            self.name = replace_list(self.prev_name, old_letter, new_letter)
        elif len(self.name) == 3:
            self.name = reverse_replace_list(self.prev_name, old_letter, new_letter, side)

    def fill_shadow_detail(self, painter, vertices, color_side, shadow):
        color = (int(color * shadow) for color in self.colors[color_side])
        painter.setBrush(QBrush(QColor(*color), Qt.SolidPattern))
        painter.fill(vertices)

    def fill_detail(self, painter, vertices, color_side):
        color = self.colors[color_side]
        # painter.setBrush(QBrush(QColor(*color), Qt.SolidPattern))
        # painter.fill(vertices)

    def draw(self, painter, visible_sides, shadows=None):
        for side in visible_sides:
            if side in self.name:
                vertices_pairs = []
                for key in self.sides[side]:
                    edge = self.edges[key]
                    start, finish = self.vertices[edge.first], self.vertices[edge.second]
                    painter.pcreate_line(start, finish)
                    vertices_pairs.append([start, finish])

                vertices = get_vertices_by_pairs(vertices_pairs)
                color_side = self.name_for_color[self.name.index(side)]

                if not shadows:
                    self.fill_detail(painter, vertices, color_side)
                else:
                    self.fill_shadow_detail(painter, vertices, color_side, shadows[side])

    def draw_turning(self, painter, visible_sides, turning_side, model_center=None, light_sources=None):
        stickers_centers = {}
        sides_vertices = {}
        for side in self.sides:
            vertices_pairs = []
            for key in self.sides[side]:
                edge = self.edges[key]
                start, finish = self.vertices[edge.first], self.vertices[edge.second]
                vertices_pairs.append([start, finish])

            vertices = get_vertices_by_pairs(vertices_pairs)
            center = 0
            for vertex in vertices:
                center += vertex.z
            center /= len(vertices)
            stickers_centers[side] = center
            sides_vertices[side] = vertices

        sides = sorted(stickers_centers, key=stickers_centers.get)
        for side in sides:
            if side in self.name:
                color_side = self.name_for_color[self.name.index(side)]
                if not light_sources:
                    self.fill_detail(painter, sides_vertices[side], color_side)
                else:
                    shadow = self.get_shadow(side, model_center, light_sources, sides_vertices[side])
                    self.fill_shadow_detail(painter, sides_vertices[side], color_side, shadow)

        opposite_side = self.cfg.get_opposite(turning_side)
        if opposite_side in visible_sides:
            self.fill_detail(painter, sides_vertices[opposite_side], 'black')

    def get_center_z(self):
        center = 0
        for vertex in self.vertices.values():
            center += vertex.z
        return center / len(self.vertices)

    def get_center_by_name(self, vertices=None):
        if not vertices:
            return None

        center = Point()

        for vertex in vertices:
            center += vertex

        return center / len(vertices)

    def get_vertex_by_name(self, name):
        set_name = set(name)
        for key in self.vertices:
            if set(key) == set_name:
                return self.vertices[key]
        return None

    def get_shadow(self, name, model_center, light_sources, vertices=None):
        if not light_sources or not vertices:
            return None

        center = self.get_center_by_name(vertices)

        plane_points = [vertices[0], *vertices[2:-1]]
        normal = Vector(MatrixPlane(plane_points).get_determinant()[:-1])
        normal.adjust(center, Point(*model_center))

        cosine = 0
        for light in light_sources:
            cosine += get_plane_cosine(light, center, normal)

        if cosine <= 1:
            return cosine
        else:
            return 1


class Corner(Detail):
    def __init__(self, vertices, edges, offset, name, model_name):
        super().__init__(vertices, edges, offset, name, model_name)


class Rib(Detail):
    def __init__(self, vertices, edges, offset, name, model_name):
        super().__init__(vertices, edges, offset, name, model_name)


class Center(Detail):
    def __init__(self, vertices, edges, offset, name, model_name):
        super().__init__(vertices, edges, offset, name, model_name, False)
        self.color = self.colors[name]

    def fill_shadow_detail(self, painter, vertices=None, color_side=None, shadow=None):
        color = (int(color * shadow) for color in self.color)
        painter.setBrush(QBrush(QColor(*color), Qt.SolidPattern))
        painter.fill(self.vertices.values())

    def fill_detail(self, painter, vertices=None, color_side=None):
        for i in range(len(self.vertices)):
            painter.pcreate_line(list(self.vertices.values())[i], list(self.vertices.values())[(i + 1) % 3])
        # painter.setBrush(QBrush(QColor(*self.color), Qt.SolidPattern))
        # painter.fill(self.vertices.values())

    def draw(self, painter, visible_sides, shadows=None):
        if not shadows:
            self.fill_detail(painter)
        else:
            self.fill_shadow_detail(painter, None, None, shadows[self.name[0]])

    def draw_turning(self, painter, visible_sides, turning_side, model_center=None, light_sources=None):
        if not light_sources:
            self.fill_detail(painter)
        else:
            shadow = self.get_shadow(self.name[0], model_center, light_sources)
            self.fill_shadow_detail(painter, None, None, shadow)

    def get_center_by_name(self, vertices=None):
        center = Point()

        for vertex in self.vertices:
            center += self.vertices[vertex]

        return center / len(self.vertices)

    def get_shadow(self, name, model_center, light_sources, vertices=None):
        if not light_sources:
            return None

        center = self.get_center_by_name()

        vertices = list(self.vertices.values())
        plane_points = [vertices[0], *vertices[2:]]

        normal = Vector(MatrixPlane(plane_points).get_determinant()[:-1])
        normal.adjust(center, Point(*model_center))

        cosine = 0
        for light in light_sources:
            cosine += get_plane_cosine(light, center, normal)

        if cosine <= 1:
            return cosine
        else:
            return 1


class Corners:
    def __init__(self, n, model_name):
        if model_name == config.CUBE:
            self.cfg = config.CubeConfig(n)
        elif model_name == config.PYRAMID:
            self.cfg = config.PyramidConfig(n)
        else:
            raise ValueError('Invalid model name param')

        self.carcass = None
        self.init_extra_points()

        vertices, edges = self.cfg.get_eccentric_data()
        positions = self.cfg.get_offset_corners()

        self.corners = {}
        for key, value in positions.items():
            self.corners[key] = Corner(deepcopy(vertices), edges, Point(*value), key, model_name)

    def init_extra_points(self):
        self.carcass = self.cfg.get_carcass()
        for key in self.carcass:
            self.carcass[key].move(config.Config().center)

    def draw(self, painter, visible_sides, shadows=None):
        for key in self.corners:
            if set(visible_sides) & set(key):
                self.corners[key].draw(painter, visible_sides, shadows)

    def draw_below_turning(self, painter, visible_sides, side, shadows=None):
        for key in self.corners:
            if set(visible_sides) & set(key) and side not in key:
                self.corners[key].draw(painter, visible_sides, shadows)

    def get_static_plastic_part(self, side, n):
        def get_carcass_vertices(src_vertices):
            vertices = []
            for vertex in src_vertices:
                set_vertex = set(vertex)
                for key in self.carcass:
                    if set_vertex == set(key):
                        vertices.append(self.carcass[key])
                        break

            return vertices

        turning_vertices = self.cfg.get_exchanges_corners()[side]
        opposite_side = self.cfg.get_opposite(side)
        below_vertices = [vertex.replace(side, opposite_side) for vertex in turning_vertices]

        upper_vertices = get_carcass_vertices(turning_vertices)
        lower_vertices = get_carcass_vertices(below_vertices)

        alpha = n - 1
        plastic_vertices = []
        for up_vertex, low_vertex in zip(upper_vertices, lower_vertices):
            plastic_vertices.append(divide_line_by_num(low_vertex, up_vertex, alpha))

        return plastic_vertices

    def get_centers(self, side):
        corners_centers = {}
        for key in self.corners:
            if side in key:
                corners_centers[self.corners[key]] = self.corners[key].get_center_z()

        return corners_centers

    def move(self, point):
        for key in self.corners:
            self.corners[key].move(point)
        for key in self.carcass:
            self.carcass[key].move(point)

    def turn_ox(self, angle):
        for key in self.corners:
            self.corners[key].turn_ox(angle)
        for key in self.carcass:
            self.carcass[key].turn_ox(angle)

    def turn_oy(self, angle):
        for key in self.corners:
            self.corners[key].turn_oy(angle)
        for key in self.carcass:
            self.carcass[key].turn_oy(angle)

    def turn_oz(self, angle):
        for key in self.corners:
            self.corners[key].turn_oz(angle)
        for key in self.carcass:
            self.carcass[key].turn_oz(angle)

    def scale(self, k, point):
        for key in self.corners:
            self.corners[key].scale(k, point)
        for key in self.carcass:
            self.carcass[key].scale(k, point)

    def turn_ox_funcs(self, sin_angle, cos_angle):
        for key in self.corners:
            self.corners[key].turn_ox_funcs(sin_angle, cos_angle)

    def turn_oy_funcs(self, sin_angle, cos_angle):
        for key in self.corners:
            self.corners[key].turn_oy_funcs(sin_angle, cos_angle)

    def turn_oz_funcs(self, sin_angle, cos_angle):
        for key in self.corners:
            self.corners[key].turn_oz_funcs(sin_angle, cos_angle)

    def turn_side_oy(self, name, angle):
        for key in self.corners:
            if name in key:
                self.corners[key].turn_oy(angle)

    def update_sides(self, side, direction):
        exchange = self.cfg.get_exchanges_corners()[side]

        dir_range = range(len(exchange) - 2, -1, -1) if direction > 0 else range(1, len(exchange))
        saved_ind = -1 if direction > 0 else 0

        tmp = self.corners[find_by_key(self.corners, exchange[saved_ind])]
        for i in dir_range:
            i_to = find_by_key(self.corners, exchange[i + direction])
            i_from = find_by_key(self.corners, exchange[i])
            self.corners[i_to] = self.corners[i_from]
            self.corners[i_to].set_name(i_to)
        self.corners[find_by_key(self.corners, exchange[saved_ind + direction])] = tmp
        self.corners[find_by_key(self.corners, exchange[saved_ind + direction])].set_name(
            find_by_key(self.corners, exchange[saved_ind + direction])
        )

        for key in self.corners:
            if side in key:
                self.corners[key].update_sides(side, direction)

    def create_plane_points(self):
        sides = self.cfg.get_sides()
        points = {}

        for key, value in sides.items():
            points[key] = [self.carcass[value[i]] for i in range(len(value))]

        return points


class Ribs:
    def __init__(self, n, model_name):
        if model_name == config.CUBE:
            self.cfg = config.CubeConfig(n)
        elif model_name == config.PYRAMID:
            self.cfg = config.PyramidConfig(n)
        else:
            raise ValueError('Invalid model name param')

        self.ribs = {}
        if n > 2:
            vertices, edges = self.cfg.get_eccentric_data()
            positions = self.cfg.get_offset_ribs()
            for key, value in positions.items():
                self.ribs[key] = []
                for position in positions[key]:
                    self.ribs[key].append(Rib(deepcopy(vertices), edges, Point(*position), key, model_name))

    def draw(self, painter, visible_sides, shadows=None):
        for key in self.ribs:
            if set(visible_sides) & set(key):
                for rib in self.ribs[key]:
                    rib.draw(painter, visible_sides, shadows)

    def draw_below_turning(self, painter, visible_sides, side, shadows=None):
        for key in self.ribs:
            if set(visible_sides) & set(key) and side not in key:
                for rib in self.ribs[key]:
                    rib.draw(painter, visible_sides, shadows)

    def get_centers(self, side):
        ribs_centers = {}
        for key in self.ribs:
            if side in key:
                for rib in self.ribs[key]:
                    ribs_centers[rib] = rib.get_center_z()

        return ribs_centers

    def move(self, point):
        for key in self.ribs:
            for rib in self.ribs[key]:
                rib.move(point)

    def turn_ox(self, angle):
        for key in self.ribs:
            for rib in self.ribs[key]:
                rib.turn_ox(angle)

    def turn_oy(self, angle):
        for key in self.ribs:
            for rib in self.ribs[key]:
                rib.turn_oy(angle)

    def turn_oz(self, angle):
        for key in self.ribs:
            for rib in self.ribs[key]:
                rib.turn_oz(angle)

    def scale(self, k, point):
        for key in self.ribs:
            for rib in self.ribs[key]:
                rib.scale(k, point)

    def turn_ox_funcs(self, sin_angle, cos_angle):
        for key in self.ribs:
            for rib in self.ribs[key]:
                rib.turn_ox_funcs(sin_angle, cos_angle)

    def turn_oy_funcs(self, sin_angle, cos_angle):
        for key in self.ribs:
            for rib in self.ribs[key]:
                rib.turn_oy_funcs(sin_angle, cos_angle)

    def turn_oz_funcs(self, sin_angle, cos_angle):
        for key in self.ribs:
            for rib in self.ribs[key]:
                rib.turn_oz_funcs(sin_angle, cos_angle)

    def turn_side_oy(self, name, angle):
        for key in self.ribs:
            if name in key:
                for rib in self.ribs[key]:
                    rib.turn_oy(angle)

    def update_sides(self, side, direction):
        exchange = self.cfg.get_exchanges_ribs()[side]

        dir_range = range(len(exchange) - 2, -1, -1) if direction > 0 else range(1, len(exchange))
        saved_ind = -1 if direction > 0 else 0

        tmp = self.ribs[find_by_key(self.ribs, exchange[saved_ind])]
        for i in dir_range:
            i_to = find_by_key(self.ribs, exchange[i + direction])
            i_from = find_by_key(self.ribs, exchange[i])
            self.ribs[i_to] = self.ribs[i_from]
            for j in range(len(self.ribs[i_to])):
                self.ribs[i_to][j].set_name(i_to)
        self.ribs[find_by_key(self.ribs, exchange[saved_ind + direction])] = tmp
        for j in range(len(self.ribs[find_by_key(self.ribs, exchange[saved_ind + direction])])):
            self.ribs[find_by_key(self.ribs, exchange[saved_ind + direction])][j].set_name(
                find_by_key(self.ribs, exchange[saved_ind + direction]))

        for key in self.ribs:
            if side in key:
                for rib in self.ribs[key]:
                    rib.update_sides(side, direction)


class Centers:
    def __init__(self, n, model_name):
        if model_name == config.CUBE:
            self.cfg = config.CubeConfig(n)
        elif model_name == config.PYRAMID:
            self.cfg = config.PyramidConfig(n)
        else:
            raise ValueError('Invalid model name param')

        self.sides_centers = None
        self.init_sides_centers()
        self.n = n

        self.centers = {}
        if n > 2 or model_name == config.PYRAMID:
            positions = self.cfg.get_offset_centers()
            for key, value in positions.items():
                vertices, edges = self.cfg.get_center_data(key)

                self.centers[key] = []
                for position in positions[key]:
                    self.centers[key].append(Center(deepcopy(vertices), edges, Point(*position), key, model_name))

    def init_sides_centers(self):
        self.sides_centers = self.cfg.get_sides_centers()
        for key in self.sides_centers:
            self.sides_centers[key].move(config.Config().center)

    def draw(self, painter, visible_sides, shadows=None):
        if self.n == 2:
            return

        for key in visible_sides:
            for center in self.centers[key]:
                center.draw(painter, visible_sides, shadows)

    def get_center(self, side):
        if self.n == 2:
            return {}

        center_centers = {}
        for center in self.centers[side]:
            center_centers[center] = center.get_center_z()

        return center_centers

    def move(self, point):
        for key in self.centers:
            for center in self.centers[key]:
                center.move(point)
        for key in self.sides_centers:
            self.sides_centers[key].move(point)

    def turn_ox(self, angle):
        for key in self.centers:
            for center in self.centers[key]:
                center.turn_ox(angle)
        for key in self.sides_centers:
            self.sides_centers[key].turn_ox(angle)

    def turn_oy(self, angle):
        for key in self.centers:
            for center in self.centers[key]:
                center.turn_oy(angle)
        for key in self.sides_centers:
            self.sides_centers[key].turn_oy(angle)

    def turn_oz(self, angle):
        for key in self.centers:
            for center in self.centers[key]:
                center.turn_oz(angle)
        for key in self.sides_centers:
            self.sides_centers[key].turn_oz(angle)

    def scale(self, k, point):
        for key in self.centers:
            for center in self.centers[key]:
                center.scale(k, point)
        for key in self.sides_centers:
            self.sides_centers[key].scale(k, point)

    def turn_ox_funcs(self, sin_angle, cos_angle):
        for key in self.centers:
            for center in self.centers[key]:
                center.turn_ox_funcs(sin_angle, cos_angle)

    def turn_oy_funcs(self, sin_angle, cos_angle):
        for key in self.centers:
            for center in self.centers[key]:
                center.turn_oy_funcs(sin_angle, cos_angle)

    def turn_oz_funcs(self, sin_angle, cos_angle):
        for key in self.centers:
            for center in self.centers[key]:
                center.turn_oz_funcs(sin_angle, cos_angle)

    def turn_side_oy(self, name, angle):
        for key in self.centers:
            if name in key:
                for rib in self.centers[key]:
                    rib.turn_oy(angle)
