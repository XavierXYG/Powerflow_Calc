import math
import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QTextEdit, QLineEdit
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



class Transformer_Dialog(Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Set Transformer Parameters')

        self.Sn_label = QLabel(self)
        self.Sn_label.move(200, 100)
        self.Sn_data = QLineEdit(self)
        self.Sn_data.move(350, 100)
        self.Sn_data.setPlaceholderText("请输入Sn(MVA)")

        self.Pk_label = QLabel(self)
        self.Pk_label.move(200, 150)
        self.Pk_data = QLineEdit(self)
        self.Pk_data.move(350, 150)
        self.Pk_data.setPlaceholderText("请输入Pk(kW)")

        self.Uk_label = QLabel(self)
        self.Uk_label.move(200, 200)
        self.Uk_data = QLineEdit(self)
        self.Uk_data.move(350, 200)
        self.Uk_data.setPlaceholderText("请输入Uk(%)")

        self.Po_label = QLabel(self)
        self.Po_label.move(200, 250)
        self.Po_data = QLineEdit(self)
        self.Po_data.move(350, 250)
        self.Po_data.setPlaceholderText("请输入Po(kW)")

        self.Io_label = QLabel(self)
        self.Io_label.move(200, 300)
        self.Io_data = QLineEdit(self)
        self.Io_data.move(350, 300)
        self.Io_data.setPlaceholderText("请输入Io(%)")

        self.Uh_label = QLabel(self)
        self.Uh_label.move(200, 350)
        self.Uh_data = QLineEdit(self)
        self.Uh_data.move(350, 350)
        self.Uh_data.setPlaceholderText("请输入Uh(kV)")

        self.Ul_label = QLabel(self)
        self.Ul_label.move(200, 400)
        self.Ul_data = QLineEdit(self)
        self.Ul_data.move(350, 400)
        self.Ul_data.setPlaceholderText("请输入Ul(kV)")


        #input content of parameter && gush these parameter outside


    def Transformer_dialog_input(self):
        TF_Dialog = []
        TF_Dlg = Transformer_Dialog()
