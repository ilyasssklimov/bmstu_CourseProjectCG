# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/design/design.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1304, 858)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(1304, 858))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.loadButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadButton.setGeometry(QtCore.QRect(1110, 110, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.loadButton.setFont(font)
        self.loadButton.setObjectName("loadButton")
        self.models = QtWidgets.QComboBox(self.centralwidget)
        self.models.setGeometry(QtCore.QRect(1110, 30, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.models.setFont(font)
        self.models.setObjectName("models")
        self.models.addItem("")
        self.models.addItem("")
        self.models.addItem("")
        self.scaleSlider = QtWidgets.QSlider(self.centralwidget)
        self.scaleSlider.setGeometry(QtCore.QRect(1110, 170, 161, 22))
        self.scaleSlider.setOrientation(QtCore.Qt.Horizontal)
        self.scaleSlider.setObjectName("scaleSlider")
        self.rotate_x = QtWidgets.QPushButton(self.centralwidget)
        self.rotate_x.setGeometry(QtCore.QRect(1170, 210, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.rotate_x.setFont(font)
        self.rotate_x.setObjectName("rotate_x")
        self.rotate_y_ = QtWidgets.QPushButton(self.centralwidget)
        self.rotate_y_.setGeometry(QtCore.QRect(1210, 250, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.rotate_y_.setFont(font)
        self.rotate_y_.setObjectName("rotate_y_")
        self.rotate_x_ = QtWidgets.QPushButton(self.centralwidget)
        self.rotate_x_.setGeometry(QtCore.QRect(1170, 250, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.rotate_x_.setFont(font)
        self.rotate_x_.setObjectName("rotate_x_")
        self.rotate_y = QtWidgets.QPushButton(self.centralwidget)
        self.rotate_y.setGeometry(QtCore.QRect(1130, 250, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.rotate_y.setFont(font)
        self.rotate_y.setObjectName("rotate_y")
        self.rotate_z = QtWidgets.QPushButton(self.centralwidget)
        self.rotate_z.setGeometry(QtCore.QRect(1210, 210, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.rotate_z.setFont(font)
        self.rotate_z.setObjectName("rotate_z")
        self.rotate_z_ = QtWidgets.QPushButton(self.centralwidget)
        self.rotate_z_.setGeometry(QtCore.QRect(1130, 210, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.rotate_z_.setFont(font)
        self.rotate_z_.setObjectName("rotate_z_")
        self.canvas = QtWidgets.QWidget(self.centralwidget)
        self.canvas.setGeometry(QtCore.QRect(30, 30, 1050, 760))
        self.canvas.setStyleSheet("border: 3px solid black ")
        self.canvas.setObjectName("canvas")
        self.gridLayout = QtWidgets.QGridLayout(self.canvas)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.right = QtWidgets.QPushButton(self.centralwidget)
        self.right.setGeometry(QtCore.QRect(1210, 320, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.right.setFont(font)
        self.right.setObjectName("right")
        self.left = QtWidgets.QPushButton(self.centralwidget)
        self.left.setGeometry(QtCore.QRect(1210, 360, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.left.setFont(font)
        self.left.setObjectName("left")
        self.up = QtWidgets.QPushButton(self.centralwidget)
        self.up.setGeometry(QtCore.QRect(1170, 320, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.up.setFont(font)
        self.up.setObjectName("up")
        self.front = QtWidgets.QPushButton(self.centralwidget)
        self.front.setGeometry(QtCore.QRect(1130, 320, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.front.setFont(font)
        self.front.setObjectName("front")
        self.sizeModel = QtWidgets.QComboBox(self.centralwidget)
        self.sizeModel.setGeometry(QtCore.QRect(1110, 70, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.sizeModel.setFont(font)
        self.sizeModel.setObjectName("sizeModel")
        self.sizeModel.addItem("")
        self.sizeModel.addItem("")
        self.sizeModel.addItem("")
        self.sizeModel.addItem("")
        self.sizeModel.addItem("")
        self.sizeModel.addItem("")
        self.sizeModel.addItem("")
        self.down = QtWidgets.QPushButton(self.centralwidget)
        self.down.setGeometry(QtCore.QRect(1170, 360, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.down.setFont(font)
        self.down.setObjectName("down")
        self.back = QtWidgets.QPushButton(self.centralwidget)
        self.back.setGeometry(QtCore.QRect(1130, 360, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.back.setFont(font)
        self.back.setObjectName("back")
        self.up_ = QtWidgets.QPushButton(self.centralwidget)
        self.up_.setGeometry(QtCore.QRect(1170, 420, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.up_.setFont(font)
        self.up_.setObjectName("up_")
        self.back_ = QtWidgets.QPushButton(self.centralwidget)
        self.back_.setGeometry(QtCore.QRect(1130, 460, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.back_.setFont(font)
        self.back_.setObjectName("back_")
        self.left_ = QtWidgets.QPushButton(self.centralwidget)
        self.left_.setGeometry(QtCore.QRect(1210, 460, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.left_.setFont(font)
        self.left_.setObjectName("left_")
        self.right_ = QtWidgets.QPushButton(self.centralwidget)
        self.right_.setGeometry(QtCore.QRect(1210, 420, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.right_.setFont(font)
        self.right_.setObjectName("right_")
        self.down_ = QtWidgets.QPushButton(self.centralwidget)
        self.down_.setGeometry(QtCore.QRect(1170, 460, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.down_.setFont(font)
        self.down_.setObjectName("down_")
        self.front_ = QtWidgets.QPushButton(self.centralwidget)
        self.front_.setGeometry(QtCore.QRect(1130, 420, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.front_.setFont(font)
        self.front_.setObjectName("front_")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1304, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.loadButton.setText(_translate("MainWindow", "Загрузить"))
        self.models.setItemText(0, _translate("MainWindow", "Кубик Рубика"))
        self.models.setItemText(1, _translate("MainWindow", "Пирамидка"))
        self.models.setItemText(2, _translate("MainWindow", "Мегаминкс"))
        self.rotate_x.setText(_translate("MainWindow", "X"))
        self.rotate_y_.setText(_translate("MainWindow", "Y\'"))
        self.rotate_x_.setText(_translate("MainWindow", "X\'"))
        self.rotate_y.setText(_translate("MainWindow", "Y"))
        self.rotate_z.setText(_translate("MainWindow", "Z"))
        self.rotate_z_.setText(_translate("MainWindow", "Z\'"))
        self.right.setText(_translate("MainWindow", "R"))
        self.left.setText(_translate("MainWindow", "L"))
        self.up.setText(_translate("MainWindow", "U"))
        self.front.setText(_translate("MainWindow", "F"))
        self.sizeModel.setItemText(0, _translate("MainWindow", "2x2x2"))
        self.sizeModel.setItemText(1, _translate("MainWindow", "3x3x3"))
        self.sizeModel.setItemText(2, _translate("MainWindow", "4x4x4"))
        self.sizeModel.setItemText(3, _translate("MainWindow", "5x5x5"))
        self.sizeModel.setItemText(4, _translate("MainWindow", "6x6x6"))
        self.sizeModel.setItemText(5, _translate("MainWindow", "7x7x7"))
        self.sizeModel.setItemText(6, _translate("MainWindow", "8x8x8"))
        self.down.setText(_translate("MainWindow", "D"))
        self.back.setText(_translate("MainWindow", "B"))
        self.up_.setText(_translate("MainWindow", "U\'"))
        self.back_.setText(_translate("MainWindow", "B\'"))
        self.left_.setText(_translate("MainWindow", "L\'"))
        self.right_.setText(_translate("MainWindow", "R\'"))
        self.down_.setText(_translate("MainWindow", "D\'"))
        self.front_.setText(_translate("MainWindow", "F\'"))
