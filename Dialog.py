import math
import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QTextEdit, QLineEdit, QComboBox
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QColor, QPen, QPainter
from PyQt5.QtCore import QLine, QPointF, QObject, pyqtSignal, pyqtSlot
from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QPalette, QIcon, QPixmap
from PyQt5 import QtGui
import qtawesome as qta

# 图元库
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem, QGraphicsPathItem
from PyQt5.QtGui import QPixmap, QPainterPath

from Dataflow import *


class Dialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(450, 650)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)  # 让放大框选项不可用

        self.setWindowOpacity(0.9)  # 设置窗口透明度
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏所有边框
        self.pe = QPalette()
        self.setAutoFillBackground(True)
        self.pe.setColor(self.backgroundRole(), QColor(3, 35, 14))  # 设置背景色
        self.setPalette(self.pe)

        self.pushbutton_close = QPushButton(self)
        self.pushbutton_close.setGeometry(QtCore.QRect(30, 20, 30, 30))
        self.pushbutton_close.setObjectName("pushButton")
        self.pushbutton_close.setStyleSheet('''QPushButton{background:#F28086;border-radius:15px;}
        QPushButton:hover{background:#F6BFC1;}''')

        self.pushbutton_mini = QPushButton(self)
        self.pushbutton_mini.setGeometry(QtCore.QRect(80, 20, 30, 30))
        self.pushbutton_mini.setObjectName("pushButton_mini")
        self.pushbutton_mini.setStyleSheet('''QPushButton{background:#8EC2F5;border-radius:15px;}
        QPushButton:hover{background:#A5DEF1;}''')

        self.set_button = QPushButton('OK', self)
        self.set_button.setStyleSheet(
            '''QPushButton{background:#007575;border-radius:5px;font-family:JetBrains Mono;font-weight:bold;}QPushButton:hover{background:green;}''')
        self.set_button.resize(80, 30)
        self.set_button.move(300, 600)

        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.setStyleSheet(
            '''QPushButton{background:#F5DEB3;border-radius:5px;font-family:JetBrains Mono;font-weight:bold;}QPushButton:hover{background:#FFD666;}''')
        self.cancel_button.resize(80, 30)
        self.cancel_button.move(400, 600)
        self.set_button.clicked.connect(self.ok_clicked)
        self.cancel_button.clicked.connect(self.cancel_clicked)

        self.pushbutton_close.clicked.connect(self.close)  # 关闭窗口
        self.pushbutton_mini.clicked.connect(self.showMinimized)  # 最小化窗口

        # 设置标签颜色，字体
        self.label_style = '''QLabel{color:white;font-size:20px;font-family:JetBrains Mono;font-weight:bold;}'''

        # 设置子类文本框背景色和字体
        bgColor = '#d7d7d7'  #文本框背景色
        self.text_style = """QLineEdit{{ color: #4C4C4C; border-width: 1px solid black;border-radius:10px;
            padding:2px 4px; background-color: {0}; color: #000000; 
                font_family:JetBrains Mono;font-weight:bold; }} 
            QLineEdit:hover{{ border: 5px solid #d7d7d7;}}""".format(
            bgColor)

        self.select_text_style = """QComboBox{{ color: #4C4C4C; border: 1px solid black;border-radius:10px;
                   padding:2px 4px; background-color: {0}; color: #000000; 
                       font_family:JetBrains Mono;font-weight:bold; }} 
                   QComboBox:hover{{ border: 0px solid #d7d7d7;}}""".format(
            bgColor)
        self.select_text_style = '''QComboBox{{ color: #4C4C4C; border: 1px solid black;border-radius:10px;
                   padding:2px 4px; background-color: {0}; color: #000000; 
                       font_family:JetBrains Mono;font-weight:bold; }} 
                   QComboBox:hover{{ border: 0px solid #d7d7d7;}}'''.format(
            bgColor)
        #setStyleSheet("QComboBox QAbstractItemView {border:1px solid #dddddd;outline:0px;height:30px;	} QComboBox QAbstractItemView::item {min-height: 30px;background-color: rgb(255, 255, 255);color:#333;padding-left:11px;outline:0px;} QComboBox QAbstractItemView::item:hover {color:#333;background-color: #e9f2ff;}"



    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

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
        self.resize(480, 300)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.PQ_text = [[]] * 2
        self.set_button.move(280, 250)
        self.cancel_button.move(380, 250)

        self.P_label = QPushButton(self)
        self.P_label.move(100, 100)
        self.P_label.setText('P(w)')
        self.P_label.setStyleSheet(self.label_style)
        self.P_data = QLineEdit(self)
        self.P_data.move(200, 100)
        self.P_data.setPlaceholderText("请输入P(w)")
        self.P_data.setStyleSheet(self.text_style)

        self.Q_label = QLabel(self)
        self.Q_label.move(100, 160)
        self.Q_label.setText('Q(var)')
        self.Q_label.setStyleSheet(self.label_style)
        self.Q_data = QLineEdit(self)
        self.Q_data.move(200, 160)
        self.Q_data.setPlaceholderText("请输入Q(var)")
        self.Q_data.setStyleSheet(self.text_style)

        self.set_button.clicked.connect(lambda: self.save_text())
        self.show()

    def save_text(self):
        self.PQ_text = [self.P_data.text(), self.Q_data.text()]
        self.close()


class PV_Dialog(Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Set PV Bus Parameters')
        self.resize(480, 300)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.PV_text = [[]] * 2

        self.set_button.move(280, 250)
        self.cancel_button.move(380, 250)

        self.P_label = QLabel(self)
        self.P_label.move(100, 100)
        self.P_label.setText('P(w)')
        self.P_label.setStyleSheet(self.label_style)
        self.P_data = QLineEdit(self)
        self.P_data.move(200, 100)
        self.P_data.setPlaceholderText("请输入P(w)")
        self.P_data.setStyleSheet(self.text_style)

        self.V_label = QLabel(self)
        self.V_label.move(100, 160)
        self.V_label.setText('V(v)')
        self.V_label.setStyleSheet(self.label_style)
        self.V_data = QLineEdit(self)
        self.V_data.move(200, 160)
        self.V_data.setPlaceholderText("请输入V(v)")
        self.V_data.setStyleSheet(self.text_style)

        self.set_button.clicked.connect(lambda: self.save_text())
        self.show()

    def save_text(self):
        self.PV_text = [self.P_data.text(), self.V_data.text()]
        self.close()


class VA_Dialog(Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Set VA Bus Parameters')
        self.resize(480, 300)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.VA_text = [[]] * 2

        self.set_button.move(280, 250)
        self.cancel_button.move(380, 250)

        self.V_label = QLabel(self)
        self.V_label.move(100, 100)
        self.V_label.setText('V(v)')
        self.V_label.setStyleSheet(self.label_style)
        self.V_data = QLineEdit(self)
        self.V_data.move(200, 100)
        self.V_data.setPlaceholderText("请输入V(v)")
        self.V_data.setStyleSheet(self.text_style)

        self.A_label = QLabel(self)
        self.A_label.move(100, 160)
        self.A_label.setText('V的辐角(度)')
        self.A_label.setStyleSheet(self.label_style)
        self.A_data = QLineEdit(self)
        self.A_data.move(200, 160)
        self.A_data.setPlaceholderText("请输入V的辐角（度）")
        self.A_data.setStyleSheet(self.text_style)

        self.set_button.clicked.connect(lambda: self.save_text())
        self.show()

    def save_text(self):
        self.VA_text = [self.V_data.text(), self.A_data.text()]
        self.close()


class Wire_Dialog(Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Set Wire Parameters')
        self.resize(650, 650)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.wire_text = [[]] * 6  # type, Dm, diameter, line_distance, length, S_wire

        self.set_button.move(450, 600)
        self.cancel_button.move(550, 600)

        self.type_label = QLabel(self)
        self.type_label.move(100, 100)
        self.type_label.setText('Type')
        self.type_label.setStyleSheet(self.label_style)
        self.type_select = QComboBox(self)
        self.type_select.move(300, 100)
        self.type_select.setStyleSheet(self.select_text_style)
        self.type_select.addItems(['type 1 :铜导线，分裂线股数为1', 'type 2 :铜导线，分裂线股数为4',
                                   'type 3 :铜导线，分裂线股数为6', 'type 4 :钢导线，分裂线股数为1',
                                   'type 5 :钢导线，分裂线股数为4', 'type 6 :钢导线，分裂线股数为6'])
        self.selected_type_index = 0

        self.D1_label = QLabel(self)
        self.D1_label.move(100, 160)
        self.D1_label.setText('D1(mm)')
        self.D1_label.setStyleSheet(self.label_style)
        self.D1_data = QLineEdit(self)
        self.D1_data.move(300, 160)
        self.D1_data.setPlaceholderText("请输入D1(mm)")
        self.D1_data.setStyleSheet(self.text_style)

        self.D2_label = QLabel(self)
        self.D2_label.move(100, 220)
        self.D2_label.setText('D2(mm)')
        self.D2_label.setStyleSheet(self.label_style)
        self.D2_data = QLineEdit(self)
        self.D2_data.move(300, 220)
        self.D2_data.setPlaceholderText("请输入D2(mm)")
        self.D2_data.setStyleSheet(self.text_style)

        self.D3_label = QLabel(self)
        self.D3_label.move(100, 280)
        self.D3_label.setText('D3(mm)')
        self.D3_label.setStyleSheet(self.label_style)
        self.D3_data = QLineEdit(self)
        self.D3_data.move(300, 280)
        self.D3_data.setPlaceholderText("请输入D3(mm)")
        self.D3_data.setStyleSheet(self.text_style)

        self.diameter_label = QLabel(self)
        self.diameter_label.move(100, 340)
        self.diameter_label.setText('传输线外直径(mm)')
        self.diameter_label.setStyleSheet(self.label_style)
        self.diameter_data = QLineEdit(self)
        self.diameter_data.move(300, 340)
        self.diameter_data.setPlaceholderText("请输入传输线直径")
        self.diameter_data.setStyleSheet(self.text_style)

        self.line_distance_label = QLabel(self)
        self.line_distance_label.move(100, 400)
        self.line_distance_label.setText('分裂线距离(mm)')
        self.line_distance_label.setStyleSheet(self.label_style)
        self.line_distance_data = QLineEdit(self)
        self.line_distance_data.move(300, 400)
        self.line_distance_data.setPlaceholderText("请输入分裂线距离")
        self.line_distance_data.setStyleSheet(self.text_style)

        self.length_label = QLabel(self)
        self.length_label.move(100, 460)
        self.length_label.setText('传输线长度(km)')
        self.length_label.setStyleSheet(self.label_style)
        self.length_data = QLineEdit(self)
        self.length_data.move(300, 460)
        self.length_data.setPlaceholderText("请输入传输线长度")
        self.length_data.setStyleSheet(self.text_style)

        self.S_wire_label = QLabel(self)
        self.S_wire_label.move(100, 520)
        self.S_wire_label.setText('传输线导通截面积')
        self.S_wire_label.setStyleSheet(self.label_style)
        self.S_wire_data = QLineEdit(self)
        self.S_wire_data.move(300, 520)
        self.S_wire_data.setPlaceholderText("请输入截面积")
        self.S_wire_data.setStyleSheet(self.text_style)

        self.wire_text = []
        self.set_button.clicked.connect(lambda: self.save_text())
        self.show()

    def selected_type(self):
        if self.type_select.highlighted():
            self.selected_type_index = self.type_select.currentIndex()

    def save_text(self):
        self.wire_text = [self.selected_type_index, self.Dm_data.text(), self.diameter_data.text(),
                          self.line_distance_data.text(),
                          self.length_data.text(), self.S_wire_data.text()]
        self.close()


class Transformer_Dialog(Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Set Transformer Parameters')
        self.resize(550, 600)

        self.tf_text = [[]] * 7

        self.set_button.move(350, 550)
        self.cancel_button.move(450, 550)

        self.Sn_label = QLabel(self)
        self.Sn_label.move(100, 100)
        self.Sn_label.setText('Sn(MVA)')
        self.Sn_label.setStyleSheet(self.label_style)
        self.Sn_data = QLineEdit(self)
        self.Sn_data.move(200, 100)
        self.Sn_data.setPlaceholderText("请输入Sn(MVA)")
        self.Sn_data.setStyleSheet(self.text_style)

        self.Pk_label = QLabel(self)
        self.Pk_label.move(100, 160)
        self.Pk_label.setText('Pk(kW)')
        self.Pk_label.setStyleSheet(self.label_style)
        self.Pk_data = QLineEdit(self)
        self.Pk_data.move(200, 160)
        self.Pk_data.setPlaceholderText("请输入Pk(kW)")
        self.Pk_data.setStyleSheet(self.text_style)

        self.Uk_label = QLabel(self)
        self.Uk_label.move(100, 220)
        self.Uk_label.setText('Uk(%)')
        self.Uk_label.setStyleSheet(self.label_style)
        self.Uk_data = QLineEdit(self)
        self.Uk_data.move(200, 220)
        self.Uk_data.setPlaceholderText("请输入Uk(%)")
        self.Uk_data.setStyleSheet(self.text_style)

        self.Po_label = QLabel(self)
        self.Po_label.move(100, 280)
        self.Po_label.setText('Po(kW)')
        self.Po_label.setStyleSheet(self.label_style)
        self.Po_data = QLineEdit(self)
        self.Po_data.move(200, 280)
        self.Po_data.setPlaceholderText("请输入Po(kW)")
        self.Po_data.setStyleSheet(self.text_style)

        self.Io_label = QLabel(self)
        self.Io_label.move(100, 340)
        self.Io_label.setText('Io(%)')
        self.Io_label.setStyleSheet(self.label_style)
        self.Io_data = QLineEdit(self)
        self.Io_data.move(200, 340)
        self.Io_data.setPlaceholderText("请输入Io(%)")
        self.Io_data.setStyleSheet(self.text_style)

        self.Uh_label = QLabel(self)
        self.Uh_label.move(100, 400)
        self.Uh_label.setText('Uh(kV)')
        self.Uh_label.setStyleSheet(self.label_style)
        self.Uh_data = QLineEdit(self)
        self.Uh_data.move(200, 400)
        self.Uh_data.setPlaceholderText("请输入Uh(kV)")
        self.Uh_data.setStyleSheet(self.text_style)

        self.Ul_label = QLabel(self)
        self.Ul_label.move(100, 460)
        self.Ul_label.setText('Ul(kV)')
        self.Ul_label.setStyleSheet(self.label_style)
        self.Ul_data = QLineEdit(self)
        self.Ul_data.move(200, 460)
        self.Ul_data.setPlaceholderText("请输入Ul(kV)")
        self.Ul_data.setStyleSheet(self.text_style)

        self.set_button.clicked.connect(lambda: self.save_text())
        self.show()

    def save_text(self):
        self.tf_text = [self.Sn_data.text(), self.Pk_data.text(), self.Uk_data.text(), self.Po_data.text(),
                        self.Io_data.text(), self.Uh_data.text(), self.Ul_data.text()]
        print(self.tf_text)
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Wire_Dialog()
    win.show()
    #print(win.tf_text)
    sys.exit(app.exec_())