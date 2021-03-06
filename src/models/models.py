from src.design.drawer import QtDrawer
from src.general.config import Config, CubeConfig, PyramidConfig, EPS, CUBE, PYRAMID
from src.models.details import Corners, Ribs, Centers
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QBrush, QColor
from src.utils.point import Point
from src.utils.matrix import MatrixPlane, MatrixBody
from src.utils.mymath import Vector, Angle, get_plane_cosine


class Model:
    def __init__(self, corners: Corners, ribs: Ribs, centers: Centers, n: int, model_name: str):
        self.n = n
        self.corners = corners
        self.ribs = ribs
        self.centers = centers

        if model_name == CUBE:
            self.cfg = CubeConfig(n)
        elif model_name == PYRAMID:
            self.cfg = PyramidConfig(n)
        else:
            raise ValueError('Invalid model name param')

        self.k = 1

        cfg = Config()
        dx, dy, dz = cfg.dx, cfg.dy, cfg.dz
        self.center_point = Point(dx, dy, dz)

        self.matrix_center = [dx, dy, dz, 1]
        self.viewer = [dx, dy, dz + 100000, 0]
        self.matrix_body = None

        self.light_sources = []

        self.visible_sides = []
        self.set_visible_sides()

    def draw(self, painter: QtDrawer) -> None:
        pen = QPen(Qt.black, 6)
        painter.setPen(pen)
        shadows = None if not self.light_sources else self.count_shadows()

        self.corners.draw(painter, self.visible_sides, shadows)
        self.ribs.draw(painter, self.visible_sides, shadows)
        self.centers.draw(painter, self.visible_sides, shadows)

    def draw_turning(self, painter: QtDrawer, side: str, plastic_part: list[Point]) -> None:
        def draw_below_turning(shadows_=None):
            self.ribs.draw_below_turning(painter, self.visible_sides, side, shadows_)
            self.centers.draw(painter, self.visible_sides, shadows_)
            self.corners.draw_below_turning(painter, self.visible_sides, side, shadows_)

        def draw_static_plastic_part():
            painter.setBrush(QBrush(QColor('black'), Qt.SolidPattern))
            painter.fill(plastic_part)

        pen = QPen(Qt.black, 6)
        painter.setPen(pen)
        shadows = None if not self.light_sources else self.count_shadows()

        if side in self.visible_sides:
            draw_below_turning(shadows)
            draw_static_plastic_part()
            self.artist(painter, side)
        else:
            self.artist(painter, side)
            draw_below_turning(shadows)

    def artist(self, painter: QtDrawer, side: str) -> None:
        corners = self.corners.get_centers(side)
        ribs = self.ribs.get_centers(side)
        centers = self.centers.get_centers(side)

        eccentric = corners | ribs | centers
        details = sorted(eccentric, key=eccentric.get)

        for detail in details:
            detail.draw_turning(painter, self.visible_sides, side, self.matrix_center[:-1], self.light_sources)

    def get_static_plastic_part(self, side: str) -> list[Point]:
        return self.corners.get_static_plastic_part(side, self.n)

    def count_shadows(self) -> dict[str, float | None]:
        shadows = {}
        for side in self.visible_sides:
            shadows[side] = self.get_shadow(side)

        return shadows

    def get_shadow(self, position_side: str) -> float | None:
        if not self.light_sources:
            return None

        side = self.cfg.get_sides()[position_side]
        center = self.centers.sides_centers[position_side]

        plane_points = [self.corners.carcass[key] for key in side]
        normal = Vector(MatrixPlane(plane_points).get_determinant()[:-1])
        normal.adjust(center, Point(*self.matrix_center[:-1]))

        cosine = 0
        for light in self.light_sources:
            cosine += get_plane_cosine(light, center, normal)

        if cosine <= 1:
            return cosine
        else:
            return 1

    def scale(self, k: float) -> None:
        k = k if k else 1
        tmp = k / self.k

        self.corners.scale(tmp, self.center_point)
        self.ribs.scale(tmp, self.center_point)
        self.centers.scale(tmp, self.center_point)

        self.k = k

    def move(self, point: Point) -> None:
        self.corners.move(point)
        self.ribs.move(point)
        self.centers.move(point)

    def turn_ox(self, angle: int | float) -> None:
        self.move(-self.center_point)

        self.corners.turn_ox(angle)
        self.ribs.turn_ox(angle)
        self.centers.turn_ox(angle)

        self.move(self.center_point)

        self.set_visible_sides()

    def turn_oy(self, angle: int | float) -> None:
        self.move(-self.center_point)

        self.corners.turn_oy(angle)
        self.ribs.turn_oy(angle)
        self.centers.turn_oy(angle)

        self.move(self.center_point)

        self.set_visible_sides()

    def turn_oz(self, angle: int | float) -> None:
        self.move(-self.center_point)

        self.corners.turn_oz(angle)
        self.ribs.turn_oz(angle)
        self.centers.turn_oz(angle)

        self.move(self.center_point)

        self.set_visible_sides()

    def turn_ox_funcs(self, sin_angle: float, cos_angle: float) -> None:
        self.corners.turn_ox_funcs(sin_angle, cos_angle)
        self.ribs.turn_ox_funcs(sin_angle, cos_angle)
        self.centers.turn_ox_funcs(sin_angle, cos_angle)

    def turn_oy_funcs(self, sin_angle: float, cos_angle: float) -> None:
        self.corners.turn_oy_funcs(sin_angle, cos_angle)
        self.ribs.turn_oy_funcs(sin_angle, cos_angle)
        self.centers.turn_oy_funcs(sin_angle, cos_angle)

    def turn_oz_funcs(self, sin_angle: float, cos_angle: float) -> None:
        self.corners.turn_oz_funcs(sin_angle, cos_angle)
        self.ribs.turn_oz_funcs(sin_angle, cos_angle)
        self.centers.turn_oz_funcs(sin_angle, cos_angle)

    def turn_side_elements(self, name: str, angle: float, alpha: Angle, beta: Angle):
        self.turn_oz_funcs(alpha.sin, alpha.cos)
        self.turn_ox_funcs(beta.sin, beta.cos)

        self.corners.turn_side_oy(name, angle)
        self.ribs.turn_side_oy(name, angle)
        self.centers.turn_side_oy(name, angle)

        self.turn_ox_funcs(-beta.sin, beta.cos)
        self.turn_oz_funcs(-alpha.sin, alpha.cos)

    def turn_side(self, name: str, angle: float) -> None:
        self.move(-self.center_point)

        direction_vector = Vector(self.centers.sides_centers[name])
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

    def update_sides(self, side: str, direction: int) -> None:
        self.corners.update_sides(side, direction)
        if self.n > 2:
            self.ribs.update_sides(side, direction)

    def set_matrix_body(self) -> None:
        sides = self.corners.create_plane_points()
        coefficients = {}

        for key, value in sides.items():
            plane = MatrixPlane(value)
            coefficients[key] = plane.get_determinant()

        self.matrix_body = MatrixBody(coefficients)
        self.matrix_body.adjust(self.matrix_center)

    def set_visible_sides(self) -> None:
        self.set_matrix_body()
        sides = self.matrix_body.sides

        visible_res = self.matrix_body.multiplication_vector(self.viewer)
        self.visible_sides = [side for side, value in zip(sides, visible_res) if value > EPS]

    def add_light(self, point: Point) -> None:
        self.light_sources.append(point)

    def del_light(self, point: Point) -> None:
        self.light_sources.remove(point)


class Cube(Model):
    def __init__(self, n: int):
        corners = Corners(n, CUBE)
        ribs = Ribs(n, CUBE)
        centers = Centers(n, CUBE)

        super().__init__(corners, ribs, centers, n, CUBE)


class Pyramid(Model):
    def __init__(self, n: int):
        corners = Corners(n, PYRAMID)
        ribs = Ribs(n, PYRAMID)
        centers = Centers(n, PYRAMID)

        self.turning_centers = None
        self.extra = None

        super().__init__(corners, ribs, centers, n, PYRAMID)

    def turn_side(self, name, angle):
        self.move(-self.center_point)

        offset = Point(self.corners.carcass[PyramidConfig().get_opposite_corners()[name]])
        self.move(-offset)

        direction_vector = Vector(self.centers.sides_centers[name])
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

        self.move(offset)
        self.move(self.center_point)

    def init_turning_centers(self, name: str) -> None:
        self.turning_centers, self.extra = self.centers.get_turning_centers(name)

    def uninit_turning_centers(self) -> None:
        self.turning_centers = None
        self.extra = None

    def update_sides(self, side: str, direction: int) -> None:
        self.corners.update_sides(side, direction)
        self.ribs.update_sides(side, direction)
        self.centers.update_sides(side, direction, self.turning_centers, self.extra)

    def turn_side_elements(self, name: str, angle: float, alpha: Angle, beta: Angle) -> None:
        self.turn_oz_funcs(alpha.sin, alpha.cos)
        self.turn_ox_funcs(beta.sin, beta.cos)

        self.corners.turn_side_oy(name, angle)
        self.ribs.turn_side_oy(name, angle)
        self.centers.turn_side_oy(name, angle, self.turning_centers)

        self.turn_ox_funcs(-beta.sin, beta.cos)
        self.turn_oz_funcs(-alpha.sin, alpha.cos)

    def draw_turning(self, painter: QtDrawer, side: str, plastic_part: list[Point]) -> None:
        def draw_below_turning(shadows_=None):
            self.ribs.draw_below_turning(painter, self.visible_sides, side, shadows_)
            self.centers.draw_below_turning(painter, self.visible_sides, self.extra, shadows_)
            self.corners.draw_below_turning(painter, self.visible_sides, side, shadows_)

        def draw_static_plastic_part():
            painter.setBrush(QBrush(QColor('black'), Qt.SolidPattern))
            painter.fill(plastic_part)

        def draw_dynamic_plastic_part():
            painter.setBrush(QBrush(QColor('black'), Qt.SolidPattern))
            painter.fill(self.corners.get_static_pyramid_plastic(side, False))

        pen = QPen(Qt.black, 6)
        painter.setPen(pen)
        shadows = None if not self.light_sources else self.count_shadows()

        if side in self.visible_sides:
            draw_below_turning(shadows)
            draw_static_plastic_part()
            self.artist(painter, side)
        else:
            self.artist(painter, side)
            draw_dynamic_plastic_part()
            draw_below_turning(shadows)

    def artist(self, painter: QtDrawer, side: str) -> None:
        corners = self.corners.get_centers(side)
        ribs = self.ribs.get_centers(side)
        centers = self.centers.get_centers(side)
        eccentric = corners | ribs | centers

        turning_centers = {}
        center_details = [center for pairs in self.turning_centers.values() for center in pairs]
        for center in center_details:
            turning_centers[center] = center.get_center_z()
        eccentric |= turning_centers

        details = sorted(eccentric, key=eccentric.get)

        for detail in details:
            detail.draw_turning(painter, self.visible_sides, side, self.matrix_center[:-1], self.light_sources)

    def get_static_plastic_part(self, side: str) -> list[Point]:
        return self.corners.get_static_pyramid_plastic(side)
