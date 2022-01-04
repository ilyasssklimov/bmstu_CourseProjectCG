from PyQt5.QtCore import QPoint

from PyQt5.QtGui import QPainter, QPolygon


class QtDrawer(QPainter):
    def create_line(self, x1, y1, x2, y2):
        self.drawLine(int(x1), int(y1), int(x2), int(y2))

    def set_pixel(self, x, y):
        self.drawLine(x, y, x + 1, y)

    def fill(self, vertices):
        points = QPolygon([QPoint(int(vertex.x), int(vertex.y)) for vertex in vertices])
        self.drawPolygon(points)
