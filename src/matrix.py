from mymath import Vector, sin_deg, cos_deg
from point import Point


class MatrixTransform:
    def __init__(self):
        self.size = 4
        self.matrix = [[0.0 for _ in range(self.size)] for _ in range(self.size)]

    def __str__(self):
        result = ''
        for i in range(self.size):
            for j in range(self.size):
                result += f'{self.matrix[i][j]:^10.1f}'
            result += '\n'

        return result

    def transpose(self):
        for i in range(self.size):
            for j in range(i + 1):
                self.matrix[i][j], self.matrix[j][i] = self.matrix[j][i], self.matrix[i][j]

    def set_move(self, point):
        for i in range(self.size):
            for j in range(self.size):
                self.matrix[i][j] = 0 if i != j else 1

        self.matrix[0][self.size - 1] = point.x
        self.matrix[1][self.size - 1] = point.y
        self.matrix[2][self.size - 1] = point.z

    def set_scale(self, k, point):
        self.set_move(point)

        for i in range(self.size - 1):
            self.matrix[i][i] = k

    def set_turn_ox(self, angle, point):
        self.set_move(point)

        self.matrix[1][1] = cos_deg(angle)
        self.matrix[1][2] = -sin_deg(angle)
        self.matrix[2][1] = sin_deg(angle)
        self.matrix[2][2] = cos_deg(angle)

    def set_turn_oy(self, angle, point):
        self.set_move(point)

        self.matrix[0][0] = cos_deg(angle)
        self.matrix[0][2] = sin_deg(angle)
        self.matrix[2][0] = -sin_deg(angle)
        self.matrix[2][2] = cos_deg(angle)

    def set_turn_oz(self, angle, point):
        self.set_move(point)

        self.matrix[0][0] = cos_deg(angle)
        self.matrix[0][1] = -sin_deg(angle)
        self.matrix[1][0] = sin_deg(angle)
        self.matrix[1][1] = cos_deg(angle)

    def set_transpose_move(self, point):
        self.set_move(point)
        self.transpose()

    def set_transpose_scale(self, k, point):
        self.set_scale(k, point)
        self.transpose()

    def set_transpose_turn_ox(self, angle, point):
        self.set_turn_ox(angle, point)
        self.transpose()

    def set_transpose_turn_oy(self, angle, point):
        self.set_turn_oy(angle, point)
        self.transpose()

    def set_transpose_turn_oz(self, angle, point):
        self.set_turn_oz(angle, point)
        self.transpose()


class MatrixPlane:
    def __init__(self, vector):
        self.matrix = []
        point_1, point_2, general = vector[0], vector[1], vector[2]

        self.matrix.append(Vector(general, Point()).get_vector())
        self.matrix.append(Vector(general, point_1).get_vector())
        self.matrix.append(Vector(general, point_2).get_vector())

    def get_minor(self, i):
        minor_matrix = [self.matrix[j][:i] + self.matrix[j][i+1:] for j in range(1, 3)]
        return minor_matrix[0][0] * minor_matrix[1][1] - minor_matrix[1][0] * minor_matrix[0][1]

    def get_determinant(self):
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
    def __init__(self, coefficients):
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

    def negative(self, i):
        self.coefficients[i] = [-coefficient for coefficient in self.coefficients[i]]

    def multiplication_vector(self, vector):
        result = []

        for i in range(self.size):
            result.append(0)
            for j in range(len(vector)):
                result[i] += vector[j] * self.coefficients[i][j]

        return result

    def multiplication(self, matrix):
        result = [[] for _ in range(self.size)]
        size = len(matrix[0])
        # TODO: ошибка если длины разные

        for i in range(len(matrix)):
            for j in range(self.size):
                result[j].append(0)
                for k in range(size):
                    result[j][i] += matrix[i][k] * self.coefficients[j][k]

        return result

    def adjust(self, point):
        result = self.multiplication_vector(point)
        for i in range(len(result)):
            if result[i] > 0:
                self.negative(i)

    def transform(self, matrix):
        self.coefficients = self.multiplication(matrix)
