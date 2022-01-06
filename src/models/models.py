from collections import Counter
from src.general.config import Config, CubeConfig, EPS
from src.models.details import Corners, Ribs, Centers, Corner, Rib, Center
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen
from src.utils.point import Point
from src.utils.matrix import MatrixPlane, MatrixBody, MatrixTransform
from src.utils.mymath import Vector, Angle
from math import asin, acos, degrees, cos


class Model:
    # TODO: добавить матрицы преобразований (и для координат, и для матрицы тела)
    def __init__(self, corners, ribs, centers, n):
        self.n = n
        self.corners = corners
        self.ribs = ribs
        self.centers = centers

        self.k = 1

        cfg = Config()
        dx, dy, dz = cfg.dx, cfg.dy, cfg.dz
        self.center_point = Point(dx, dy, dz)

        self.matrix_center = [dx, dy, dz, 1]
        self.viewer = [dx, dy, dz + 100000, 0]
        self.matrix_body = None
        self.visible_sides = []
        self.set_visible_sides()

    def draw(self, painter):
        pen = QPen(Qt.black, 6)
        painter.setPen(pen)

        self.corners.draw(painter, self.visible_sides)
        self.ribs.draw(painter, self.visible_sides)
        self.centers.draw(painter, self.visible_sides)

    def draw_turning(self, painter, side):
        # TODO: красить полностью грань перед поворачиваемой
        pen = QPen(Qt.black, 6)
        painter.setPen(pen)

        self.ribs.draw_below_turning(painter, self.visible_sides, side)
        self.corners.draw_below_turning(painter, self.visible_sides, side)
        self.centers.draw(painter, self.visible_sides)

        self.artist(painter, side)

    def artist(self, painter, side):
        # Если противоположная сторона грани видна, то черным

        corners = self.corners.get_centers(side)
        ribs = self.ribs.get_centers(side)
        centers = self.centers.get_center(side)
        eccentric = corners | ribs | centers
        details = sorted(eccentric, key=eccentric.get)

        for detail in details:
            if not isinstance(detail, Center):
                detail.draw_turning(painter)
            else:
                detail.draw(painter, [side])
        '''
        for key in details:
            if len(key) == 2:
                for rib in self.ribs.ribs[key]:
                    rib.draw_turning(painter)
            elif len(key) == 3:
                self.corners.corners[key].draw_turning(painter)
            else:
                for center in self.centers.centers[key]:
                    center.draw(painter, [side])
        '''
        # print(self.centers.get_center(side))
        # self.centers.draw(painter, [side])

    def scale(self, k):
        k = k if k else 1
        tmp = k / self.k

        self.corners.scale(tmp, self.center_point)
        self.ribs.scale(tmp, self.center_point)
        self.centers.scale(tmp, self.center_point)

        self.k = k

    def move(self, point):
        self.corners.move(point)
        self.ribs.move(point)
        self.centers.move(point)

    def turn_ox(self, angle):
        self.move(-self.center_point)

        self.corners.turn_ox(angle)
        self.ribs.turn_ox(angle)
        self.centers.turn_ox(angle)

        self.move(self.center_point)

        self.set_visible_sides()

    def turn_oy(self, angle):
        self.move(-self.center_point)

        self.corners.turn_oy(angle)
        self.ribs.turn_oy(angle)
        self.centers.turn_oy(angle)

        self.move(self.center_point)

        self.set_visible_sides()

    def turn_oz(self, angle):
        self.move(-self.center_point)

        self.corners.turn_oz(angle)
        self.ribs.turn_oz(angle)
        self.centers.turn_oz(angle)

        self.move(self.center_point)

        self.set_visible_sides()

    def turn_ox_funcs(self, sin_angle, cos_angle):
        self.corners.turn_ox_funcs(sin_angle, cos_angle)
        self.ribs.turn_ox_funcs(sin_angle, cos_angle)
        self.centers.turn_ox_funcs(sin_angle, cos_angle)

    def turn_oy_funcs(self, sin_angle, cos_angle):
        self.corners.turn_oy_funcs(sin_angle, cos_angle)
        self.ribs.turn_oy_funcs(sin_angle, cos_angle)
        self.centers.turn_oy_funcs(sin_angle, cos_angle)

    def turn_oz_funcs(self, sin_angle, cos_angle):
        self.corners.turn_oz_funcs(sin_angle, cos_angle)
        self.ribs.turn_oz_funcs(sin_angle, cos_angle)
        self.centers.turn_oz_funcs(sin_angle, cos_angle)

    def turn_side_elements(self, name, angle, alpha, beta):
        self.turn_oz_funcs(alpha.sin, alpha.cos)
        self.turn_ox_funcs(beta.sin, beta.cos)

        self.corners.turn_side_oy(name, angle)
        self.ribs.turn_side_oy(name, angle)
        self.centers.turn_side_oy(name, angle)

        self.turn_ox_funcs(-beta.sin, beta.cos)
        self.turn_oz_funcs(-alpha.sin, alpha.cos)

    def turn_side(self, name, angle):
        self.move(-self.center_point)

        direction_vector = Vector(Point(0, 0, 0), self.centers.sides_centers[name])
        direction_vector.normalize()
        d = direction_vector.get_length_xy()

        alpha = Angle()  # to yz plane
        beta = Angle()  # to y
        try:
            alpha.set_cos(direction_vector.y / d)
            alpha.set_sin(direction_vector.x / d)
        except ZeroDivisionError:
            alpha.set_cos(1)
            alpha.set_sin(0)
        beta.set_cos(d)
        beta.set_sin(-direction_vector.z)

        self.turn_side_elements(name, angle, alpha, beta)

        self.move(self.center_point)

    def update_sides(self, side, direction):
        self.corners.update_sides(side, direction)
        if self.n > 2:
            self.ribs.update_sides(side, direction)

    def set_matrix_body(self):
        sides = self.corners.create_plane_points()
        coefficients = {}

        for key, value in sides.items():
            plane = MatrixPlane(value)
            coefficients[key] = plane.get_determinant()

        self.matrix_body = MatrixBody(coefficients)
        self.matrix_body.adjust(self.matrix_center)

    def set_visible_sides(self):
        self.set_matrix_body()
        result = self.matrix_body.multiplication_vector(self.viewer)
        sides = self.matrix_body.sides
        self.visible_sides = [side for side, value in zip(sides, result) if value > EPS]


class Cube(Model):
    def __init__(self, n):
        corners = Corners(n)
        ribs = Ribs(n)
        centers = Centers(n)

        super().__init__(corners, ribs, centers, n)
