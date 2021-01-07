import math
import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QTextEdit, QLineEdit, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QColor, QPen, QPainter
from PyQt5.QtCore import QLine, QPointF, QObject, pyqtSignal, pyqtSlot
from PyQt5 import QtCore

# 图元库
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem, QGraphicsPathItem
from PyQt5.QtGui import QPixmap, QPainterPath

from Dataflow import *


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
        self.dialog_dataflow = []


    def ok_clicked(self):
        pass

    def cancel_clicked(self):  #
        self.close()

    def show_dialog(self):
        self.show()


class PQ_Dialog(Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Set PQ Bus Parameters')
        self.resize(800, 400)

        self.tf_text = [[]] * 2

        self.P_label = QLabel(self)
        self.P_label.move(200, 100)
        self.P_label.setText('P(Mw)')
        self.P_data = QLineEdit(self)
        self.P_data.move(300, 100)
        self.P_data.setPlaceholderText("请输入P(mw)")

        self.Q_label = QLabel(self)
        self.Q_label.move(200, 160)
        self.Q_label.setText('Q(Mvar)')
        self.Q_data = QLineEdit(self)
        self.Q_data.move(300, 160)
        self.Q_data.setPlaceholderText("请输入Q(Mvar)")

        self.set_button.clicked.connect(lambda: self.save_text())
        self.PQ_dataflow = []     #save the text
        self.dialog_PQ = []       #build and save the dialog

        # input content of parameter && push these parameter outside


    def save_text(self):
        self.PQ_text = [self.P_data.text(), self.Q_data.text()]
        new_dataflow_PQ = Dataflow.df_PQ(self.PQ_text)
        Dataflow.pull(new_dataflow_PQ)
        self.PQ_dataflow.append(new_dataflow_PQ)
        self.close()
        print(self.PQ_dataflow)

    def show_dialog(self):
        self.show()



class PV_Dialog(Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Set PV Bus Parameters')
        self.resize(800, 400)

        self.tf_text = [[]] * 2

        self.P_label = QLabel(self)
        self.P_label.move(200, 100)
        self.P_label.setText('P(Mw)')
        self.P_data = QLineEdit(self)
        self.P_data.move(300, 100)
        self.P_data.setPlaceholderText("请输入P(mw)")

        self.V_label = QLabel(self)
        self.V_label.move(200, 160)
        self.V_label.setText('V(kv)')
        self.V_data = QLineEdit(self)
        self.V_data.move(300, 160)
        self.V_data.setPlaceholderText("请输入V(kv)")

        self.set_button.clicked.connect(lambda: self.save_text())
        self.PV_dataflow = []     #save the text
        self.dialog_PV = []       #build and save the dialog

        # input content of parameter && push these parameter outside


    def save_text(self):
        self.PV_text = [self.P_data.text(), self.V_data.text()]
        new_dataflow_PV = Dataflow.df_PQ(self.PV_text)
        Dataflow.pull(new_dataflow_PV)
        self.PV_dataflow.append(new_dataflow_PV)
        self.close()
        print(self.PV_dataflow)

    def show_dialog(self):
        self.show()


class VA_Dialog(Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Set VA Bus Parameters')
        self.resize(800, 400)

        self.tf_text = [[]] * 2

        self.V_label = QLabel(self)
        self.V_label.move(200, 100)
        self.V_label.setText('V(kv)')
        self.V_data = QLineEdit(self)
        self.V_data.move(300, 100)
        self.V_data.setPlaceholderText("请输入V(kv)")

        self.V_label = QLabel(self)
        self.V_label.move(200, 160)
        self.V_label.setText('V的辐角(度)')
        self.V_data = QLineEdit(self)
        self.V_data.move(300, 160)
        self.V_data.setPlaceholderText("请输入V的辐角（度）")

        self.set_button.clicked.connect(lambda: self.save_text())
        self.VA_dataflow = []     #save the text
        self.dialog_VA = []       #build and save the dialog

        # input content of parameter && push these parameter outside


    def save_text(self):
        self.VA_text = [self.V_data.text(), self.A_data.text()]
        new_dataflow_VA = Dataflow.df_PQ(self.VA_text)
        Dataflow.pull(new_dataflow_VA)
        self.VA_dataflow.append(new_dataflow_VA)
        self.close()
        print(self.VA_dataflow)

    def show_dialog(self):
        self.show()


class Wire_Dialog(Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Set Wire Parameters')
        self.resize(800, 800)

        self.tf_text = [[]] * 6  #type, Dm, diameter, line_distance, length, S_wire

        self.type_label = QLabel(self)
        self.type_label.move(200, 100)
        self.type_label.setText('Type')
        self.type_select = QComboBox(self)
        self.type_select.move(400, 100)
        self.type_select.addItems(['type 1 :铜导线，分裂线股数为1','type 2 :铜导线，分裂线股数为4',
                                   'type 3 :铜导线，分裂线股数为6', 'type 4 :钢导线，分裂线股数为1',
                                   'type 5 :钢导线，分裂线股数为4', 'type 6 :钢导线，分裂线股数为6'])
        self.selected_type_store = []

        self.Dm_label = QLabel(self)
        self.Dm_label.move(200, 160)
        self.Dm_label.setText('Dm(mm)')
        self.Dm_data = QLineEdit(self)
        self.Dm_data.move(400, 160)
        self.Dm_data.setPlaceholderText("请输入Dm(mm)")

        self.diameter_label = QLabel(self)
        self.diameter_label.move(200, 220)
        self.diameter_label.setText('传输线外直径(mm)')
        self.diameter_data = QLineEdit(self)
        self.diameter_data.move(400, 220)
        self.diameter_data.setPlaceholderText("请输入传输线外直径")

        self.line_distance_label = QLabel(self)
        self.line_distance_label.move(200, 280)
        self.line_distance_label.setText('分裂线距离(mm)')
        self.line_distance_data = QLineEdit(self)
        self.line_distance_data.move(400, 280)
        self.line_distance_data.setPlaceholderText("请输入分裂线距离")

        self.length_label = QLabel(self)
        self.length_label.move(200, 340)
        self.length_label.setText('传输线长度(km)')
        self.length_data = QLineEdit(self)
        self.length_data.move(400, 340)
        self.length_data.setPlaceholderText("请输入传输线长度")

        self.S_wire_label = QLabel(self)
        self.S_wire_label.move(200, 400)
        self.S_wire_label.setText('传输线导通截面积')
        self.S_wire_data = QLineEdit(self)
        self.S_wire_data.move(400, 400)
        self.S_wire_data.setPlaceholderText("请输入传输线截面积")


        self.set_button.clicked.connect(lambda: self.save_text())
        self.wire_dataflow = []
        self.dialog_wire = []

        # input content of parameter && push these parameter outside

    def selected_type(self):
        if self.type_select.highlighted():
            self.selected_type_store = self.type_select.currentIndex()
            print(self.type_select.highlighted[int])

    def show_dialog(self):
        self.show()

    def save_text(self):
        self.wire_text = [self.type_select.currentIndexChanged[int], self.Dm_data.text(), self.diameter_data.text(), self.line_distance_data.text(),
                        self.length_data.text(), self.S_wire_data.text()]
        new_dataflow_wire = Dataflow.df_wire(self.wire_text)
        Dataflow.pull(new_dataflow_wire)
        self.wire_dataflow.append(new_dataflow_wire)
        print(self.type_select.currentIndexChanged[int])
        self.close()
        print(self.wire_dataflow)


class Transformer_Dialog(Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Set Transformer Parameters')
        self.resize(800, 800)

        self.tf_text = [[]] * 7

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

        self.set_button.clicked.connect(lambda: self.save_text())
        self.tf_dataflow = []
        self.dialog_tf = []

        # input content of parameter && push these parameter outside

    def show_dialog(self):
        self.show()

    def save_text(self):
        self.tf_text = [self.Sn_data.text(), self.Pk_data.text(), self.Uk_data.text(), self.Po_data.text(),
                        self.Io_data.text(), self.Uh_data.text(), self.Ul_data.text()]
        new_dataflow_edge = Dataflow.df_transformer(self.tf_text)
        Dataflow.pull(new_dataflow_edge)
        self.tf_dataflow.append(new_dataflow_edge)

        self.close()
        print(self.tf_dataflow)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Wire_Dialog()
    win.show()
    sys.exit(app.exec_())
