from typing import ValuesView

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter, QPolygon
from src.utils.point import Point


class QtDrawer(QPainter):
    def create_line(self, x1: float | int, y1: float | int, x2: float | int, y2: float | int) -> None:
        self.drawLine(int(x1), int(y1), int(x2), int(y2))

    def pcreate_line(self, point_1: Point, point_2: Point) -> None:
        self.drawLine(int(point_1.x), int(point_1.y), int(point_2.x), int(point_2.y))

    def set_pixel(self, x: float | int, y: float | int) -> None:
        self.drawPoint(int(x), int(y))

    def pset_pixel(self, point: Point) -> None:
        self.drawPoint(int(point.x), int(point.y))

    def fill(self, vertices: list[Point] | ValuesView[Point]) -> None:
        points = QPolygon([QPoint(int(vertex.x), int(vertex.y)) for vertex in vertices])
        self.drawPolygon(points)
