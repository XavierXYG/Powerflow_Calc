import math
import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QColor, QPen, QPainter
from PyQt5.QtCore import QLine, QPointF

# 图元库
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem, QGraphicsPathItem
from PyQt5.QtGui import QPixmap, QPainterPath


class Dialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(600, 300)
        # self.setWindowIcon('./dialog_icon.jpg')

        self.set_button = QPushButton(self)
        self.set_button.setText('OK')
        self.set_button.resize(40, 15)
        self.set_button.move(500, 250)

        self.cancel_button = QPushButton(self)
        self.cancel_button.setText('Cancel')
        self.cancel_button.resize(40, 15)
        self.cancel_button.move(550, 250)


class PQ_Dialog(Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Set PQ Bus Parameters')

        self.P_label = QLabel(self)
        self.P_label.move(200, 100)

        self.Q_label = QLabel(self)
        self.Q_label.move(200, 150)
