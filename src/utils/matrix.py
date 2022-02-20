from src.utils.mymath import Vector
from src.utils.point import Point


class MatrixPlane:
    def __init__(self, vector: list[float]):
        self.matrix = []
        point_1, point_2, general = vector[0], vector[1], vector[2]

        self.matrix.append(Vector(general, Point()).get_vector())
        self.matrix.append(Vector(general, point_1).get_vector())
        self.matrix.append(Vector(general, point_2).get_vector())

    def get_minor(self, i: int) -> float:
        minor_matrix = [self.matrix[j][:i] + self.matrix[j][i+1:] for j in range(1, 3)]
        return minor_matrix[0][0] * minor_matrix[1][1] - minor_matrix[1][0] * minor_matrix[0][1]

    def get_determinant(self) -> list[float]:
        result = []
        d = 0

        for i in range(3):
            minor = self.get_minor(i)
            if i == 1:
                minor *= -1
            result.append(minor)
            tmp = self.matrix[0][i] * minor
            d += tmp

        result.append(d)
        return result


class MatrixBody:
    def __init__(self, coefficients: dict[str, list[float]]):
        self.sides = coefficients.keys()
        self.coefficients = list(coefficients.values())
        self.size = len(self.coefficients)

    def __str__(self):
        result = ''
        for i in range(len(self.coefficients[0])):
            for j in range(self.size):
                result += f'{self.coefficients[j][i]:^14.1f}'
            result += '\n'

        return result

    def negative(self, i: int) -> None:
        self.coefficients[i] = [-coefficient for coefficient in self.coefficients[i]]

    def multiplication_vector(self, vector: list[float]) -> list[float]:
        result = []

        for i in range(self.size):
            result.append(0)
            for j in range(len(vector)):
                result[i] += vector[j] * self.coefficients[i][j]

        return result

    def multiplication(self, matrix: list[list[float]]) -> list[list[float]]:
        result = [[] for _ in range(self.size)]
        size = len(matrix[0])

        for i in range(len(matrix)):
            for j in range(self.size):
                result[j].append(0)
                for k in range(size):
                    result[j][i] += matrix[i][k] * self.coefficients[j][k]

        return result

    def adjust(self, point: list[float]) -> None:
        result = self.multiplication_vector(point)
        for i in range(len(result)):
            if result[i] > 0:
                self.negative(i)

    def transform(self, matrix: list[list[float]]) -> None:
        self.coefficients = self.multiplication(matrix)
