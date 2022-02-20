from src.utils.point import Point


class Edge:
    def __init__(self, first: str, second: str):
        self.first = first
        self.second = second

    def __str__(self):
        return f'Edge({self.first}, {self.second})'

    def __repr__(self):
        return str(self)

    def get_points(self, vertices: dict[str, Point]) -> tuple[Point, Point]:
        return vertices[self.first], vertices[self.second]

    def __contains__(self, item):
        if isinstance(item, list):
            for i in item:
                if i in self.first and i in self.second:
                    return True
            return False
        else:
            return item in self.first and item in self.second
