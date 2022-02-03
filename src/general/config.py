from math import sqrt
from src.utils.edge import Edge
from src.general.errors import SideNameError
from src.utils.point import Point


EPS = 1e5
SHADOW = 0.15
CUBE = 'Кубик Рубика'
PYRAMID = 'Пирамидка'
MEGAMINX = 'Мегаминкс'


class Config:
    def __init__(self):
        self.size = 150

        self.main_width = 1304
        self.main_height = 858

        self.width = 1050
        self.height = 760
        self.offset_x = 30
        self.offset_y = 30

        self.dx = self.width / 2 + self.offset_x
        self.dy = self.height / 2 + self.offset_y
        self.dz = 0
        self.center = Point(self.dx, self.dy, self.dz)

        self.right_light = Point(self.dx + 1000, self.dy, self.dz + 1000)
        self.left_light = Point(self.dx - 1000, self.dy, self.dz + 1000)


def get_colors(mode='standard'):
    match mode:
        case 'standard':
            return {
                'R': 'red',
                'L': 'orange',
                'U': 'blue',
                'D': 'green',
                'F': 'white',
                'B': 'yellow'
            }
        case _:
            raise ValueError('Incorrect mode to get colors')


class CubeConfig:
    def __init__(self, n=3):
        self.n = n
        self.size = Config().size / self.n

    def get_center_data(self, name):
        match name:
            case 'L':
                vertices = {
                    'LFD': (-self.size, self.size, self.size),
                    'LFU': (-self.size, -self.size, self.size),
                    'LBU': (-self.size, -self.size, -self.size),
                    'LBD': (-self.size, self.size, -self.size)
                }
                edges = [
                    ('LFD', 'LFU'),
                    ('LFU', 'LBU'),
                    ('LBU', 'LBD'),
                    ('LBD', 'LFD')
                ]
            case 'R':
                vertices = {
                    'RFD': (self.size, self.size, self.size),
                    'RFU': (self.size, -self.size, self.size),
                    'RBU': (self.size, -self.size, -self.size),
                    'RBD': (self.size, self.size, -self.size)
                }
                edges = [
                    ('RFD', 'RFU'),
                    ('RFU', 'RBU'),
                    ('RBU', 'RBD'),
                    ('RBD', 'RFD')
                ]
            case 'F':
                vertices = {
                    'LFD': (-self.size, self.size, self.size),
                    'LFU': (-self.size, -self.size, self.size),
                    'RFU': (self.size, -self.size, self.size),
                    'RFD': (self.size, self.size, self.size)
                }
                edges = [
                    ('LFD', 'LFU'),
                    ('LFU', 'RFU'),
                    ('RFU', 'RFD'),
                    ('RFD', 'LFD')
                ]
            case 'B':
                vertices = {
                    'LBD': (-self.size, self.size, -self.size),
                    'LBU': (-self.size, -self.size, -self.size),
                    'RBU': (self.size, -self.size, -self.size),
                    'RBD': (self.size, self.size, -self.size)
                }
                edges = [
                    ('LBD', 'LBU'),
                    ('LBU', 'RBU'),
                    ('RBU', 'RBD'),
                    ('RBD', 'LBD')
                ]
            case 'U':
                vertices = {
                    'LBU': (-self.size, -self.size, -self.size),
                    'LFU': (-self.size, -self.size, self.size),
                    'RFU': (self.size, -self.size, self.size),
                    'RBU': (self.size, -self.size, -self.size)
                }
                edges = [
                    ('LBU', 'LFU'),
                    ('LFU', 'RFU'),
                    ('RFU', 'RBU'),
                    ('RBU', 'LBU')
                ]
            case 'D':
                vertices = {
                    'LBD': (-self.size, self.size, -self.size),
                    'LFD': (-self.size, self.size, self.size),
                    'RFD': (self.size, self.size, self.size),
                    'RBD': (self.size, self.size, -self.size)
                }
                edges = [
                    ('LBD', 'LFD'),
                    ('LFD', 'RFD'),
                    ('RFD', 'RBD'),
                    ('RBD', 'LBD')
                ]
            case _:
                raise SideNameError

        vertices = {key: Point(*vertex) for key, vertex in vertices.items()}
        edges = [Edge(*edge) for edge in edges]

        return vertices, edges

    def get_eccentric_data(self):
        vertices = {
            'LFD': (-self.size, self.size, self.size),
            'LFU': (-self.size, -self.size, self.size),
            'RFU': (self.size, -self.size, self.size),
            'RFD': (self.size, self.size, self.size),

            'LBD': (-self.size, self.size, -self.size),
            'LBU': (-self.size, -self.size, -self.size),
            'RBU': (self.size, -self.size, -self.size),
            'RBD': (self.size, self.size, -self.size)
        }
        vertices = {key: Point(*vertex) for key, vertex in vertices.items()}

        edges = {
            'LF': ('LFD', 'LFU'),
            'UF': ('LFU', 'RFU'),
            'RF': ('RFU', 'RFD'),
            'DF': ('RFD', 'LFD'),

            'LD': ('LFD', 'LBD'),
            'LU': ('LFU', 'LBU'),
            'RU': ('RFU', 'RBU'),
            'RD': ('RFD', 'RBD'),

            'LB': ('LBD', 'LBU'),
            'UB': ('LBU', 'RBU'),
            'RB': ('RBU', 'RBD'),
            'DB': ('RBD', 'LBD')
        }
        edges = {key: Edge(*edge) for key, edge in edges.items()}

        return vertices, edges

    def get_eccentric_detail_sides(self):
        sides = {
            'U': ('UF', 'LU', 'RU', 'UB'),
            'D': ('DF', 'LD', 'RD', 'DB'),
            'R': ('RF', 'RU', 'RD', 'RB'),
            'L': ('LF', 'LD', 'LU', 'LB'),
            'F': ('LF', 'UF', 'RF', 'DF'),
            'B': ('LB', 'UB', 'RB', 'DB')
        }

        return sides

    def get_offset_corners(self):
        offset = Config().size * (self.n - 1) / self.n
        positions = {
            'LFD': (-offset, offset, offset),
            'LFU': (-offset, -offset, offset),
            'RFU': (offset, -offset, offset),
            'RFD': (offset, offset, offset),

            'LBD': (-offset, offset, -offset),
            'LBU': (-offset, -offset, -offset),
            'RBU': (offset, -offset, -offset),
            'RBD': (offset, offset, -offset)
        }

        return positions

    def get_offset_ribs(self):
        if self.n < 3:
            return None

        def add(position, value, axis):
            position.append(value)
            if axis == 'x':
                position.append((-value[0], value[1], value[2]))
            elif axis == 'y':
                position.append((value[0], -value[1], value[2]))
            elif axis == 'z':
                position.append((value[0], value[1], -value[2]))

        edges = ['RF', 'UF', 'LF', 'DF', 'RU', 'RD', 'LD', 'LU', 'RB', 'UB', 'LB', 'DB']
        positions = {edge: [] for edge in edges}

        offset = Config().size * (self.n - 1) / self.n
        if self.n % 2:
            positions['RF'].append((offset, 0, offset))
            positions['UF'].append((0, -offset, offset))
            positions['LF'].append((-offset, 0, offset))
            positions['DF'].append((0, offset, offset))

            positions['RU'].append((offset, -offset, 0))
            positions['RD'].append((offset, offset, 0))
            positions['LD'].append((-offset, offset, 0))
            positions['LU'].append((-offset, -offset, 0))

            positions['RB'].append((offset, 0, -offset))
            positions['UB'].append((0, -offset, -offset))
            positions['LB'].append((-offset, 0, -offset))
            positions['DB'].append((0, offset, -offset))

        n = (self.n - 2) // 2
        step = self.size
        t = 1 if not self.n % 2 else 2

        for i in range(n):
            addition = (i * 2 + t) * step

            add(positions['RF'], (offset, addition, offset), 'y')
            add(positions['UF'], (addition, -offset, offset), 'x')
            add(positions['LF'], (-offset, addition, offset), 'y')
            add(positions['DF'], (addition, offset, offset), 'x')

            add(positions['RU'], (offset, -offset, addition), 'z')
            add(positions['RD'], (offset, offset, addition), 'z')
            add(positions['LD'], (-offset, offset, addition), 'z')
            add(positions['LU'], (-offset, -offset, addition), 'z')

            add(positions['RB'], (offset, addition, -offset), 'y')
            add(positions['UB'], (addition, -offset, -offset), 'x')
            add(positions['LB'], (-offset, addition, -offset), 'y')
            add(positions['DB'], (addition, offset, -offset), 'x')

        return positions

    def get_offset_centers(self):
        n = self.n - 2

        sides = ['R', 'L', 'U', 'D', 'F', 'B']
        positions = {side: [] for side in sides}

        offset = Config().size * (self.n - 1) / self.n
        step = self.size
        t = 1 if not self.n % 2 else 0

        for i in range(-(n // 2), (n + 1) // 2):
            dy = (i * 2 + t) * step
            for j in range(-(n // 2), (n + 1) // 2):
                dx = (j * 2 + t) * step

                positions['F'].append((dx, dy, offset))
                positions['B'].append((dx, dy, -offset))
                positions['R'].append((offset, dy, dx))
                positions['L'].append((-offset, dy, dx))
                positions['U'].append((dx, -offset, dy))
                positions['D'].append((dx, offset, dy))

        return positions

    def get_sides_centers(self):
        offset = Config().size
        sides_centers = {
            'R': (offset, 0, 0),
            'L': (-offset, 0, 0),
            'U': (0, -offset, 0),
            'D': (0, offset, 0),
            'F': (0, 0, offset),
            'B': (0, 0, -offset)
        }
        sides_centers = {side: Point(*center) for side, center in sides_centers.items()}

        return sides_centers

    def get_exchanges_corners(self):
        exchanges_corners = {
            'R': ['RFU', 'RBU', 'RBD', 'RFD'],
            'L': ['LFU', 'LFD', 'LBD', 'LBU'],
            'U': ['ULF', 'ULB', 'URB', 'URF'],
            'D': ['DLF', 'DRF', 'DRB', 'DLB'],
            'F': ['FLU', 'FRU', 'FRD', 'FLD'],
            'B': ['BLU', 'BLD', 'BRD', 'BRU']
        }

        return exchanges_corners

    def get_exchanges_ribs(self):
        exchanges_ribs = {
            'R': ['RU', 'RB', 'RD', 'RF'],
            'L': ['LU', 'LF', 'LD', 'LB'],
            'U': ['UF', 'UL', 'UB', 'UR'],
            'D': ['DF', 'DR', 'DB', 'DL'],
            'F': ['FU', 'FR', 'FD', 'FL'],
            'B': ['BU', 'BL', 'BD', 'BR']
        }

        return exchanges_ribs

    def get_exchanges_centers(self):
        exchanges_centers = {
            'R': ['U', 'B', 'D', 'F'],
            'L': ['U', 'F', 'D', 'B'],
            'U': ['F', 'L', 'B', 'R'],
            'D': ['F', 'R', 'B', 'L'],
            'F': ['U', 'R', 'D', 'L'],
            'B': ['U', 'L', 'D', 'R']
        }

        return exchanges_centers

    def get_carcass(self):
        size = Config().size
        vertices = {
            'LFD': (-size, size, size),
            'RFD': (size, size, size),
            'RFU': (size, -size, size),
            'LFU': (-size, -size, size),

            'LBD': (-size, size, -size),
            'RBD': (size, size, -size),
            'RBU': (size, -size, -size),
            'LBU': (-size, -size, -size),
        }
        vertices = {key: Point(*vertex) for key, vertex in vertices.items()}

        return vertices

    def get_sides(self):
        # you can choose another
        sides = {
            'U': ('LFU', 'RBU', 'RFU'),
            'D': ('LFD', 'RBD', 'RFD'),
            'R': ('RFD', 'RBU', 'RBD'),
            'L': ('LFD', 'LBU', 'LBD'),
            'F': ('LFD', 'RFU', 'LFU'),
            'B': ('LBD', 'RBU', 'LBU')
        }

        return sides

    def get_opposite(self, side):
        sides = {
            'U': 'D',
            'D': 'U',
            'R': 'L',
            'L': 'R',
            'F': 'B',
            'B': 'F'
        }
        return sides[side]

    def get_center_colors(self):
        colors = {
            'F': (255, 255, 255),
            'B': (255, 255, 0),
            'R': (255, 0, 0),
            'L': (255, 165, 0),
            'U': (0, 0, 255),
            'D': (0, 128, 0),
            'black': (0, 0, 0)
        }

        return colors


class PyramidConfig:
    def __init__(self, n=3):
        self.n = n
        self.size = Config().size / self.n

    def get_eccentric_data(self):
        a = self.size * 3
        h_pyr = a * sqrt(2 / 3)
        r_inner = a / (2 * sqrt(3))

        vertices = {
            'LRF': (0, -h_pyr / 2, 0),
            'LFD': (-a / 2, h_pyr / 2, r_inner),
            'RFD': (a / 2, h_pyr / 2, r_inner),
            'LRD': (0, h_pyr / 2, -r_inner * 2)
        }
        vertices = {key: Point(*vertex) for key, vertex in vertices.items()}

        edges = {
            'LF': ('LRF', 'LFD'),
            'RF': ('LRF', 'RFD'),
            'LR': ('LRF', 'LRD'),

            'FD': ('LFD', 'RFD'),
            'RD': ('RFD', 'LRD'),
            'LD': ('LFD', 'LRD'),
        }
        edges = {key: Edge(*edge) for key, edge in edges.items()}

        return vertices, edges

    def get_offset_corners(self):
        offset = Config().size * (self.n - 1) / self.n
        a = offset * 3
        h_pyr = a * sqrt(2 / 3)
        r_inner = a / (2 * sqrt(3))

        positions = {
            'LRF': (0, -h_pyr * 2 / 3, 0),
            'LFD': (-a / 2, h_pyr / 3, r_inner),
            'RFD': (a / 2, h_pyr / 3, r_inner),
            'LRD': (0, h_pyr / 3, -r_inner * 2)
        }

        return positions

    def get_eccentric_detail_sides(self):
        sides = {
            'L': ('LF', 'LR', 'LD'),
            'F': ('LF', 'RF', 'FD'),
            'R': ('RF', 'LR', 'RD'),
            'D': ('FD', 'RD', 'LD')
        }

        return sides

    def get_offset_ribs(self):
        if self.n < 3:
            return None

        def append_rib(position, pair):
            position.append((
                pair[1][0] + (pair[0][0] - pair[1][0]) * i / (n + 1),
                pair[1][1] + (pair[0][1] - pair[1][1]) * i / (n + 1),
                pair[1][2] + (pair[0][2] - pair[1][2]) * i / (n + 1)
            ))

        edges = ['LF', 'RF', 'LR', 'FD', 'RD', 'LD']
        positions = {edge: [] for edge in edges}

        n = self.n - 2
        corners = self.get_offset_corners()

        pairs_corners = {
            'LF': (corners['LFD'], corners['LRF']),
            'RF': (corners['RFD'], corners['LRF']),
            'LR': (corners['LRD'], corners['LRF']),
            'FD': (corners['RFD'], corners['LFD']),
            'RD': (corners['RFD'], corners['LRD']),
            'LD': (corners['LFD'], corners['LRD'])
        }
        for i in range(1, n + 1):
            for edge in edges:
                append_rib(positions[edge], pairs_corners[edge])

        return positions

    def get_center_data(self, name):
        a = self.size * 3
        h_pyr = a * sqrt(2 / 3)
        r_inner = a / (2 * sqrt(3))

        match name:
            case 'F':
                vertices = {
                    'LRF': (0, h_pyr / 2, 0),
                    'LFD': (-a / 2, -h_pyr / 2, r_inner),
                    'RFD': (a / 2, -h_pyr / 2, r_inner)
                }

                edges = [
                    ('LRF', 'LFD'),
                    ('LRF', 'RFD'),
                    ('LFD', 'RFD')
                ]

            case 'L':
                vertices = {
                    'LRF': (0, h_pyr / 2, 0),
                    'LFD': (-a / 2, -h_pyr / 2, r_inner),
                    'LRD': (0, -h_pyr / 2, -r_inner * 2)
                }

                edges = [
                    ('LRF', 'LFD'),
                    ('LRF', 'LRD'),
                    ('LFD', 'LRD'),
                ]

            case 'R':
                vertices = {
                    'LRF': (0, h_pyr / 2, 0),
                    'RFD': (a / 2, -h_pyr / 2, r_inner),
                    'LRD': (0, -h_pyr / 2, -r_inner * 2)
                }

                edges = [
                    ('LRF', 'RFD'),
                    ('LRF', 'LRD'),
                    ('RFD', 'LRD')
                ]

            case 'D':
                vertices = {
                    'LFD': (-a / 2, -h_pyr / 2, r_inner),
                    'RFD': (a / 2, -h_pyr / 2, r_inner),
                    'LRD': (0, -h_pyr / 2, -r_inner * 2)
                }

                edges = [
                    ('LFD', 'RFD'),
                    ('RFD', 'LRD'),
                    ('LFD', 'LRD'),
                ]

            case _:
                raise SideNameError

        vertices = {key: Point(*vertex) for key, vertex in vertices.items()}
        edges = [Edge(*edge) for edge in edges]

        return vertices, edges

    def get_offset_centers(self):
        '''
        def append_rib(position, pair):
            position.append((
                pair[1][0] + (pair[0][0] - pair[1][0]) * i / (n + 1),
                pair[1][1] + (pair[0][1] - pair[1][1]) * i / (n + 1),
                pair[1][2] + (pair[0][2] - pair[1][2]) * i / (n + 1)
            ))

        edges = ['LF', 'RF', 'LR', 'FD', 'RD', 'LD']
        positions = {edge: [] for edge in edges}

        n = (self.n - 2)
        corners = self.get_offset_corners()

        pairs_corners = {
            'LF': (corners['LFD'], corners['LRF']),
            'RF': (corners['RFD'], corners['LRF']),
            'LR': (corners['LRD'], corners['LRF']),
            'FD': (corners['RFD'], corners['LFD']),
            'RD': (corners['RFD'], corners['LRD']),
            'LD': (corners['LFD'], corners['LRD'])
        }
        for i in range(1, n + 1):
            for edge in edges:
                append_rib(positions[edge], pairs_corners[edge])

        '''
        n = self.n - 2

        sides = ['F', 'L', 'R', 'D']
        positions = {side: [] for side in sides}
        corners = self.get_carcass()

        offset = Config().size * (self.n - 1) / self.n
        step = self.size
        t = 1 if not self.n % 2 else 0

        for i in range(-(n // 2), (n + 1) // 2):
            dy = (i * 2 + t) * step
            for j in range(-(n // 2), (n + 1) // 2):
                dx = (j * 2 + t) * step

                positions['F'].append((dx, dy, offset))
                positions['B'].append((dx, dy, -offset))
                positions['R'].append((offset, dy, dx))
                positions['L'].append((-offset, dy, dx))
                positions['U'].append((dx, -offset, dy))
                positions['D'].append((dx, offset, dy))

        return positions

    def get_center_colors(self):
        colors = {
            'F': (255, 255, 255),
            'R': (255, 0, 0),
            'L': (255, 165, 0),
            'D': (0, 128, 0),
            'black': (0, 0, 0)
        }

        return colors

    def get_carcass(self):
        a = Config().size * 3
        h_pyr = a * sqrt(2 / 3)
        r_inner = a / (2 * sqrt(3))

        vertices = {
            'LRF': (0, -h_pyr / 2, 0),
            'LFD': (-a / 2, h_pyr / 2, r_inner),
            'RFD': (a / 2, h_pyr / 2, r_inner),
            'LRD': (0, h_pyr / 2, -r_inner * 2)
        }

        vertices = {key: Point(*vertex) for key, vertex in vertices.items()}

        return vertices


    '''
    def get_sides_centers(self):
        offset = Config().size
        sides_centers = {
            'R': (offset, 0, 0),
            'L': (-offset, 0, 0),
            'U': (0, -offset, 0),
            'D': (0, offset, 0),
            'F': (0, 0, offset),
            'B': (0, 0, -offset)
        }
        sides_centers = {side: Point(*center) for side, center in sides_centers.items()}

        return sides_centers

    def get_exchanges_corners(self):
        exchanges_corners = {
            'R': ['RFU', 'RBU', 'RBD', 'RFD'],
            'L': ['LFU', 'LFD', 'LBD', 'LBU'],
            'U': ['ULF', 'ULB', 'URB', 'URF'],
            'D': ['DLF', 'DRF', 'DRB', 'DLB'],
            'F': ['FLU', 'FRU', 'FRD', 'FLD'],
            'B': ['BLU', 'BLD', 'BRD', 'BRU']
        }

        return exchanges_corners

    def get_exchanges_ribs(self):
        exchanges_ribs = {
            'R': ['RU', 'RB', 'RD', 'RF'],
            'L': ['LU', 'LF', 'LD', 'LB'],
            'U': ['UF', 'UL', 'UB', 'UR'],
            'D': ['DF', 'DR', 'DB', 'DL'],
            'F': ['FU', 'FR', 'FD', 'FL'],
            'B': ['BU', 'BL', 'BD', 'BR']
        }

        return exchanges_ribs

    def get_exchanges_centers(self):
        exchanges_centers = {
            'R': ['U', 'B', 'D', 'F'],
            'L': ['U', 'F', 'D', 'B'],
            'U': ['F', 'L', 'B', 'R'],
            'D': ['F', 'R', 'B', 'L'],
            'F': ['U', 'R', 'D', 'L'],
            'B': ['U', 'L', 'D', 'R']
        }

        return exchanges_centers

    def get_sides(self):
        # you can choose another
        sides = {
            'U': ('LFU', 'RBU', 'RFU'),
            'D': ('LFD', 'RBD', 'RFD'),
            'R': ('RFD', 'RBU', 'RBD'),
            'L': ('LFD', 'LBU', 'LBD'),
            'F': ('LFD', 'RFU', 'LFU'),
            'B': ('LBD', 'RBU', 'LBU')
        }

        return sides

    def get_opposite(self, side):
        sides = {
            'U': 'D',
            'D': 'U',
            'R': 'L',
            'L': 'R',
            'F': 'B',
            'B': 'F'
        }
        return sides[side]

    '''