from math import sqrt
from src.utils.mymath import sin_deg, cos_deg


class Point:
    def __init__(self, x: float | int = 0, y: float | int = 0, z: float | int = 0):
        if isinstance(x, Point):
            self.x = x.x
            self.y = x.y
            self.z = x.z
        elif isinstance(x, int | float):
            self.x = x
            self.y = y
            self.z = z
        else:
            raise ValueError('Invalid params to point constructor')

    def __str__(self):
        return f'Point({self.x}, {self.y}, {self.z})'

    def __repr__(self):
        return str(self)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self):
        return Point(-self.x, -self.y, -self.z)

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other, self.z / other)

    def __itruediv__(self, other):
        self.x /= other
        self.y /= other
        self.z /= other
        return self

    def __abs__(self):
        return Point(abs(self.x), abs(self.y), abs(self.z))

    def move(self, point) -> None:
        self.x += point.x
        self.y += point.y
        self.z += point.z

    def scale(self, k: float, point) -> None:
        self.x = point.x + (self.x - point.x) * k
        self.y = point.y + (self.y - point.y) * k
        self.z = point.z + (self.z - point.z) * k

    def turn_ox(self, angle: float) -> None:
        y, z = self.y, self.z
        self.y = y * cos_deg(angle) - z * sin_deg(angle)
        self.z = y * sin_deg(angle) + z * cos_deg(angle)

    def turn_oy(self, angle: float) -> None:
        x, z = self.x, self.z
        self.x = x * cos_deg(angle) + z * sin_deg(angle)
        self.z = -x * sin_deg(angle) + z * cos_deg(angle)

    def turn_oz(self, angle: float) -> None:
        x, y = self.x, self.y
        self.x = x * cos_deg(angle) - y * sin_deg(angle)
        self.y = x * sin_deg(angle) + y * cos_deg(angle)

    def turn_ox_funcs(self, sin_angle: float, cos_angle: float) -> None:
        y, z = self.y, self.z
        self.y = y * cos_angle - z * sin_angle
        self.z = y * sin_angle + z * cos_angle

    def turn_oy_funcs(self, sin_angle: float, cos_angle: float) -> None:
        x, z = self.x, self.z
        self.x = x * cos_angle + z * sin_angle
        self.z = -x * sin_angle + z * cos_angle

    def turn_oz_funcs(self, sin_angle: float, cos_angle: float) -> None:
        x, y = self.x, self.y
        self.x = x * cos_angle - y * sin_angle
        self.y = x * sin_angle + y * cos_angle

    def get_homogenous_point(self) -> list[float | int]:
        return [self.x, self.y, self.z, 1]

    def get_homogenous_vector(self) -> list[float | int]:
        return [self.x, self.y, self.z, 0]

    def negative(self) -> None:
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z

    def get_dist_to_point(self, point) -> float:
        return sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2 + (self.z - point.z) ** 2)


def divide_line_by_num(point_1: Point, point_2: Point, alpha: float) -> Point:
    return Point(
        (point_1.x + alpha * point_2.x) / (1 + alpha),
        (point_1.y + alpha * point_2.y) / (1 + alpha),
        (point_1.z + alpha * point_2.z) / (1 + alpha),
    )
