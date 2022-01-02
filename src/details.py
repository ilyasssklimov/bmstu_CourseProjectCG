from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor, QBrush

import config
from copy import deepcopy
from mymath import find_by_key, add_repeats, get_vertices_by_pairs
from point import Point


# TODO: наследовать детали от одного класса
# TODO: убрать дублирование кода, рефакторинг!


class Detail:
    def __init__(self, vertices, edges, offset, name, eccentric=True):
        self.vertices = vertices
        self.edges = edges
        self.name = None
        self.set_name(name)
        self.name_for_color = list(name)
        # self.name_to_color.sort()
        self.colors = config.CubeConfig().get_center_colors()
        if eccentric:
            self.sides = config.CubeConfig().get_eccentric_detail_sides()

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
        self.name = list(name)
        # self.name.sort()

    def update_sides(self, side, direction):
        exchange = config.CubeConfig().get_exchanges_centers()[side]

        dir_range = range(len(exchange) - 2, -1, -1) if direction > 0 else range(1, len(exchange))
        saved_ind = -1 if direction > 0 else 0

        tmp = self.sides[exchange[saved_ind]]
        for i in dir_range:
            i_to = exchange[i + direction]
            i_from = exchange[i]
            self.sides[i_to] = self.sides[i_from]
        self.sides[exchange[saved_ind + direction]] = tmp

        print('============================')
        print('====BEFORE====')
        print(f'{self.name = }, {self.name_for_color = }')
        if self.name[0] != self.name_for_color[0] and self.name[1] != self.name_for_color[1]:
            self.name[0], self.name[1] = self.name[1], self.name[0]
        print('====AFTER=====')
        print(f'{self.name = }, {self.name_for_color = }')
        print('============================')

    def fill_detail(self, painter, vertices, side):
        painter.setBrush(QBrush(QColor(self.colors[side]), Qt.SolidPattern))
        painter.fill(vertices)

    def draw(self, painter, visible_sides):
        for side in visible_sides:
            if side in self.name:
                vertices_pairs = []
                for key in self.sides[side]:
                    edge = self.edges[key]
                    start, finish = self.vertices[edge.first], self.vertices[edge.second]
                    vertices_pairs.append([start, finish])
                    # print(key)
                    # painter.create_line(start.x, start.y, finish.x, finish.y)

                vertices = get_vertices_by_pairs(vertices_pairs)
                # print(f'{side = }')
                # if side == 'U':
                #     print(f'{self.name = }')
                #     print(f'{self.name_for_color = }')

                # print(self.name)
                # print(self.name_to_color)
                # print('-' * 10)
                self.fill_detail(painter, vertices, self.name_for_color[self.name.index(side)])


class Corner(Detail):
    def __init__(self, vertices, edges, offset, name):
        super().__init__(vertices, edges, offset, name)


class Rib(Detail):
    def __init__(self, vertices, edges, offset, name):
        super().__init__(vertices, edges, offset, name)


class Center(Detail):
    def __init__(self, vertices, edges, offset, name):
        super().__init__(vertices, edges, offset, name)
        self.color = self.colors[name]

    def fill_detail(self, painter, vertices=None, side=None):
        painter.setBrush(QBrush(QColor(self.color), Qt.SolidPattern))
        painter.fill(self.vertices.values())

    def draw(self, painter, visible_sides=None):
        # for edge in self.edges:
        # start, finish = self.vertices[edge.first], self.vertices[edge.second]
        # painter.create_line(start.x, start.y, finish.x, finish.y)
        self.fill_detail(painter)


class Corners:
    def __init__(self, n):
        self.carcass = self.init_carcass()

        cfg = config.CubeConfig(n)
        vertices, edges = cfg.get_eccentric_data()
        positions = cfg.get_offset_corners()

        self.corners = {}
        for key, value in positions.items():
            self.corners[key] = Corner(deepcopy(vertices), edges, Point(*value), key)

    def init_carcass(self):
        carcass = config.CubeConfig().get_carcass()
        for key in carcass:
            carcass[key].move(config.Config().center)

        return carcass

    def draw(self, painter, visible_sides):
        for key in self.corners:
            if set(visible_sides) & set(key):
                self.corners[key].draw(painter, visible_sides)

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
        exchange = config.CubeConfig().get_exchanges_corners()[side]

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
        sides = config.CubeConfig().get_sides()
        points = {}

        for key, value in sides.items():
            points[key] = [self.carcass[value[i]] for i in range(len(value))]

        return points


class Ribs:
    def __init__(self, n):
        self.ribs = {}
        if n > 2:
            cfg = config.CubeConfig(n)
            vertices, edges = cfg.get_eccentric_data()
            positions = cfg.get_offset_ribs()
            for key, value in positions.items():
                self.ribs[key] = []
                for position in positions[key]:
                    self.ribs[key].append(Rib(deepcopy(vertices), edges, Point(*position), key))

    def draw(self, painter, visible_sides):
        for key in self.ribs:
            if set(visible_sides) & set(key):
                for rib in self.ribs[key]:
                    rib.draw(painter, visible_sides)

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
        exchange = config.CubeConfig().get_exchanges_ribs()[side]

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
    def __init__(self, n):
        self.sides_centers = self.init_sides_centers()
        self.n = n

        self.centers = {}
        if n > 2:
            cfg = config.CubeConfig(n)
            positions = cfg.get_offset_centers()
            for key, value in positions.items():
                vertices, edges = cfg.get_center_data(key)
                self.centers[key] = []
                for position in positions[key]:
                    self.centers[key].append(Center(deepcopy(vertices), edges, Point(*position), key))

    def init_sides_centers(self):
        sides_centers = config.CubeConfig().get_sides_centers()
        for key in sides_centers:
            sides_centers[key].move(config.Config().center)

        return sides_centers

    def draw(self, painter, visible_sides):
        if self.n > 2:
            for key in visible_sides:
                for center in self.centers[key]:
                    center.draw(painter)

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
