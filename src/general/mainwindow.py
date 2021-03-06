import PyQt5.QtGui
from PyQt5.QtCore import QRect, QPoint
from PyQt5.QtGui import QColor, QRadialGradient, QBrush
from PyQt5 import QtWidgets, QtCore

from src.general.config import Config, get_colors, CUBE, PYRAMID
from src.design.design import Ui_MainWindow
from src.design.drawer import QtDrawer
from src.models.models import Cube, Pyramid
from src.utils.mymath import sign
from src.utils.point import Point


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.image = QRect(
            Config().offset_x + 3,
            Config().offset_y + 3,
            Config().width - 3,
            Config().height - 3
        )
        self.gradient = QRadialGradient(QPoint(int(Config().dx), int(Config().dy)), 600)
        self.gradient.setColorAt(0, QColor('lightgrey'))
        self.gradient.setColorAt(1, QColor('grey'))

        self.model = None
        self.k_step = 80
        self.k = self.k_step
        self.angle = 10
        self.speed = 2
        self.angle_to_turn = 90

        self.models.setCurrentText(CUBE)
        self.sizeModel.setCurrentText('3x3x3')
        self.load_model()

        self.x = 0
        self.y = 0
        self.cfg = Config()
        self.viewer = Point(self.cfg.dx, self.cfg.dy, self.cfg.dz)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.turn_side)
        self.duration = 0
        self.turning_side = ''
        self.turning_direction = 0
        self.plastic_vertices = None

        self.loadButton.clicked.connect(self.load_model)
        self.scaleSlider.valueChanged.connect(self.scale_model)
        self.models.currentTextChanged.connect(self.load_model)
        self.sizeModel.currentTextChanged.connect(self.load_model)

        self.set_connects_to_buttons()
        self.change_turn_buttons_color()

        self.turning_keys = {
            QtCore.Qt.Key_Q: ('L', 1),
            QtCore.Qt.Key_W: ('U', 1),
            QtCore.Qt.Key_E: ('R', 1),
            QtCore.Qt.Key_A: ('L', -1),
            QtCore.Qt.Key_S: ('U', -1),
            QtCore.Qt.Key_D: ('R', -1)
        }

        self.right_light_point = Config().right_light
        self.left_light_point = Config().left_light

    def set_connects_to_buttons(self):
        self.rotate_y_.clicked.connect(lambda: self.turn_model_oy(self.angle))
        self.rotate_y.clicked.connect(lambda: self.turn_model_oy(-self.angle))
        self.rotate_x.clicked.connect(lambda: self.turn_model_ox(self.angle))
        self.rotate_x_.clicked.connect(lambda: self.turn_model_ox(-self.angle))
        self.rotate_z.clicked.connect(lambda: self.turn_model_oz(self.angle))
        self.rotate_z_.clicked.connect(lambda: self.turn_model_oz(-self.angle))

        self.right.clicked.connect(lambda: self.start_turning_side('R', 1))
        self.up.clicked.connect(lambda: self.start_turning_side('U', 1))
        self.front.clicked.connect(lambda: self.start_turning_side('F', 1))
        self.left.clicked.connect(lambda: self.start_turning_side('L', 1))
        self.down.clicked.connect(lambda: self.start_turning_side('D', 1))
        self.back.clicked.connect(lambda: self.start_turning_side('B', 1))

        self.right_.clicked.connect(lambda: self.start_turning_side('R', -1))
        self.up_.clicked.connect(lambda: self.start_turning_side('U', -1))
        self.front_.clicked.connect(lambda: self.start_turning_side('F', -1))
        self.left_.clicked.connect(lambda: self.start_turning_side('L', -1))
        self.down_.clicked.connect(lambda: self.start_turning_side('D', -1))
        self.back_.clicked.connect(lambda: self.start_turning_side('B', -1))

        self.right_light.stateChanged.connect(self.change_right_light)
        self.left_light.stateChanged.connect(self.change_left_light)

    def change_turn_buttons_color(self, mode='standard'):
        colors = get_colors(mode)

        self.right.setStyleSheet(f'border : 2px solid black;\nborder-radius : 8px;\nbackground-color : {colors["R"]}')
        self.right_.setStyleSheet(f'border : 2px solid black;\nborder-radius : 8px;\nbackground-color : {colors["R"]}')

        self.up.setStyleSheet(f'border : 2px solid black;\nborder-radius : 8px;\nbackground-color : {colors["U"]}')
        self.up_.setStyleSheet(f'border : 2px solid black;\nborder-radius : 8px;\nbackground-color : {colors["U"]}')

        self.front.setStyleSheet(f'border : 2px solid black;\nborder-radius : 8px;\nbackground-color : {colors["F"]}')
        self.front_.setStyleSheet(f'border : 2px solid black;\nborder-radius : 8px;\nbackground-color : {colors["F"]}')

        self.left.setStyleSheet(f'border : 2px solid black;\nborder-radius : 8px;\nbackground-color : {colors["L"]}')
        self.left_.setStyleSheet(f'border : 2px solid black;\nborder-radius : 8px;\nbackground-color : {colors["L"]}')

        self.down.setStyleSheet(f'border : 2px solid black;\nborder-radius : 8px;\nbackground-color : {colors["D"]}')
        self.down_.setStyleSheet(f'border : 2px solid black;\nborder-radius : 8px;\nbackground-color : {colors["D"]}')

        self.back.setStyleSheet(f'border : 2px solid black;\nborder-radius : 8px;\nbackground-color : {colors["B"]}')
        self.back_.setStyleSheet(f'border : 2px solid black;\nborder-radius : 8px;\nbackground-color : {colors["B"]}')

    def load_model(self) -> None:
        self.scaleSlider.setValue(self.k_step)
        self.k = self.k_step
        model = self.models.currentText()
        self.right_light.setCheckState(False)
        self.left_light.setCheckState(False)

        if model == CUBE:
            size = int(self.sizeModel.currentText().split('x')[0])
            self.model = Cube(size)
            self.angle_to_turn = 90

            self.model.turn_oy(45)
            self.model.turn_ox(-30)

            self.update()

        elif model == PYRAMID:
            self.sizeModel.setCurrentText('3x3x3')
            size = int(self.sizeModel.currentText().split('x')[0])
            self.model = Pyramid(size)

            self.angle_to_turn = 120

            self.model.turn_oy(60)
            self.model.turn_ox(-30)

            self.update()

    def paintEvent(self, event: PyQt5.QtGui.QPaintEvent) -> None:
        painter = QtDrawer()
        painter.begin(self)

        brush = QBrush(self.gradient)
        painter.setBrush(brush)
        painter.drawRect(self.image)

        if self.duration == 0:
            self.model.draw(painter)
        else:
            self.model.draw_turning(painter, self.turning_side, self.plastic_vertices)

        painter.end()

    def scale_model(self) -> None:
        if not self.model or self.k == self.scaleSlider.value():
            return

        self.k = self.scaleSlider.value()
        if self.k < 1:
            self.k = 1

        self.model.scale(self.k / self.k_step)
        self.update()

    def wheelEvent(self, event: PyQt5.QtGui.QWheelEvent) -> None:
        if not self.model:
            return

        self.k += event.angleDelta().y() / 120
        if self.k < 1:
            self.k = 1
        elif self.k > 100:
            self.k = 100

        self.scaleSlider.setValue(int(self.k))
        self.model.scale(self.k / self.k_step)
        self.update()

    def turn_model_ox(self, angle: int) -> None:
        self.model.turn_ox(angle)
        self.update()

    def turn_model_oy(self, angle: int) -> None:
        self.model.turn_oy(angle)
        self.update()

    def turn_model_oz(self, angle: int) -> None:
        self.model.turn_oz(angle)
        self.update()

    def mousePressEvent(self, event: PyQt5.QtGui.QMouseEvent) -> None:
        if self.x != event.x() or self.y != event.y():
            self.x, self.y = event.x(), event.y()

    def mouseMoveEvent(self, event: PyQt5.QtGui.QMouseEvent) -> None:
        if self.duration != 0:
            return

        x1, y1 = event.x(), event.y()
        dx, dy = sign(x1 - self.x) * self.speed, sign(self.y - y1) * self.speed

        modifiers = QtWidgets.QApplication.keyboardModifiers()

        if modifiers == QtCore.Qt.ShiftModifier:
            self.turn_model_oz(dx)
        elif event.buttons() == QtCore.Qt.RightButton:
            if dx:
                self.turn_model_oy(dx)
            if dy:
                self.turn_model_ox(dy)

        self.x, self.y = x1, y1

    def set_turning_params(self, name: str, direction: int) -> None:
        self.turning_side = name
        self.turning_direction = direction

    def start_turning_side(self, name: str, direction: int) -> None:
        if isinstance(self.model, Pyramid) and (name == 'B' or name == 'U'):
            return

        if self.duration == 0:
            self.plastic_vertices = self.model.get_static_plastic_part(name)
            self.set_turning_params(name, direction)
            if isinstance(self.model, Pyramid):
                self.model.init_turning_centers(name)
            self.timer.start(0)

    def turn_side(self) -> None:
        self.duration += 1
        self.model.turn_side(self.turning_side, self.turning_direction)

        if self.duration >= self.angle_to_turn:
            self.update_sides()
            if isinstance(self.model, Pyramid):
                self.model.uninit_turning_centers()
            self.timer.stop()
            self.duration = 0

        self.update()

    def update_sides(self) -> None:
        self.model.update_sides(self.turning_side, self.turning_direction)

    def keyPressEvent(self, event: PyQt5.QtGui.QKeyEvent) -> None:
        key = PyQt5.QtCore.Qt.Key(event.key())

        if key in self.turning_keys and self.duration == 0:
            self.start_turning_side(*self.turning_keys[key])

    def add_light_source(self, point: Point) -> None:
        self.model.add_light(point)
        self.update()

    def delete_light_source(self, point: Point) -> None:
        self.model.del_light(point)
        self.update()

    def change_right_light(self) -> None:
        if self.right_light.isChecked():
            self.add_light_source(self.right_light_point)
        else:
            self.delete_light_source(self.right_light_point)

    def change_left_light(self) -> None:
        if self.left_light.isChecked():
            self.add_light_source(self.left_light_point)
        else:
            self.delete_light_source(self.left_light_point)
