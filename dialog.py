import math
import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QTextEdit, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QColor, QPen, QPainter
from PyQt5.QtCore import QLine, QPointF,QObject , pyqtSignal, pyqtSlot
from PyQt5 import QtCore

# 图元库
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem, QGraphicsPathItem
from PyQt5.QtGui import QPixmap, QPainterPath

from Edge import QT_wire, QT_transformer


class Dialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(750, 650)
        # self.setWindowIcon('./dialog_icon.jpg')

        self.set_button = QPushButton('OK', self)
        self.set_button.resize(70, 20)
        self.set_button.move(600, 600)

        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.resize(70, 20)
        self.cancel_button.move(700, 600)
        self.set_button.clicked.connect(self.ok_clicked)
        self.cancel_button.clicked.connect(self.cancel_clicked)

    def ok_clicked(self):
        pass

    def cancel_clicked(self):        #
        self.close()


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
        self.resize(800, 800)

        self.tf_text = [[]]*7


        self.Sn_label = QLabel(self)
        self.Sn_label.move(200, 100)
        self.Sn_label.setText('Sn(MVA)')
        self.Sn_data = QLineEdit(self)
        self.Sn_data.move(300, 100)
        self.Sn_data.setPlaceholderText("请输入Sn(MVA)")

        self.Pk_label = QLabel(self)
        self.Pk_label.move(200, 160)
        self.Pk_label.setText('Pk(kW)')
        self.Pk_data = QLineEdit(self)
        self.Pk_data.move(300, 160)
        self.Pk_data.setPlaceholderText("请输入Pk(kW)")


        self.Uk_label = QLabel(self)
        self.Uk_label.move(200, 220)
        self.Uk_label.setText('Uk(%)')
        self.Uk_data = QLineEdit(self)
        self.Uk_data.move(300, 220)
        self.Uk_data.setPlaceholderText("请输入Uk(%)")


        self.Po_label = QLabel(self)
        self.Po_label.move(200, 280)
        self.Po_label.setText('Po(kW)')
        self.Po_data = QLineEdit(self)
        self.Po_data.move(300, 280)
        self.Po_data.setPlaceholderText("请输入Po(kW)")


        self.Io_label = QLabel(self)
        self.Io_label.move(200, 340)
        self.Io_label.setText('Io(%)')
        self.Io_data = QLineEdit(self)
        self.Io_data.move(300, 340)
        self.Io_data.setPlaceholderText("请输入Io(%)")


        self.Uh_label = QLabel(self)
        self.Uh_label.move(200, 400)
        self.Uh_label.setText('Uh(kV)')
        self.Uh_data = QLineEdit(self)
        self.Uh_data.move(300, 400)
        self.Uh_data.setPlaceholderText("请输入Uh(kV)")


        self.Ul_label = QLabel(self)
        self.Ul_label.move(200, 460)
        self.Ul_label.setText('Ul(kV)')
        self.Ul_data = QLineEdit(self)
        self.Ul_data.move(300, 460)
        self.Ul_data.setPlaceholderText("请输入Ul(kV)")

        self.set_button.clicked.connect(lambda: self.set_text())
        self.set_text()
        self.tf_dataflow = []


        #input content of parameter && push these parameter outside


    def set_text(self):
        self.tf_text = [self.Sn_data.text(), self.Pk_data.text(), self.Uk_data.text(), self.Po_data.text(),
                        self.Io_data.text(), self.Uh_data.text(), self.Ul_data.text()]
        new_edge = QT_transformer(self.tf_text)
        #Dataflow.pull(new_edge)
        self.tf_dataflow.append(new_edge)

        self.close()
        print(self.tf_dataflow)




if __name__ == '__main__':
    app=QApplication(sys.argv)
    win=Transformer_Dialog()
    win.show()
    sys.exit(app.exec_())
