import math
import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QTextEdit, QLineEdit, QComboBox, QToolTip
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
        # self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)  # 让放大框选项不可用

        # 设置窗口背景
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏所有边框
        self.pe = QPalette()
        self.setAutoFillBackground(True)
        self.pe.setColor(self.backgroundRole(), QColor(88, 87, 86))  # 设置背景色
        self.setPalette(self.pe)

        # 设置提示语画板
        QToolTip.setFont(QFont('JetBrain Mono', 9))
        self.tool_bgd = QToolTip.palette()
        self.tool_bgd.setColor(self.tool_bgd.Inactive, self.tool_bgd.ToolTipBase, QColor(3, 35, 14))
        self.tool_bgd.setColor(self.tool_bgd.Inactive, self.tool_bgd.ToolTipText, QColor(102, 102, 255))

        self.pushbutton_close = QPushButton(self)
        self.pushbutton_close.setGeometry(QtCore.QRect(30, 20, 30, 30))
        self.pushbutton_close.setObjectName("pushButton")
        self.pushbutton_close.setStyleSheet('''QPushButton{background:#F28086;border-radius:15px;}
        QPushButton:hover{background:#F6BFC1;}''')

        self.pushbutton_close.setToolTip('<b>Close</b>')
        self.setAutoFillBackground(True)
        self.pushbutton_close.setPalette(self.pe)

        self.pushbutton_mini = QPushButton(self)
        self.pushbutton_mini.setGeometry(QtCore.QRect(80, 20, 30, 30))
        self.pushbutton_mini.setObjectName("pushButton_mini")
        self.pushbutton_mini.setStyleSheet('''QPushButton{background:#8EC2F5;border-radius:15px;}
        QPushButton:hover{background:#A5DEF1;}''')
        self.pushbutton_mini.setToolTip('<b>Minimize</b>')

        self.set_button = QPushButton('OK', self)
        self.set_button.setStyleSheet(
            '''QPushButton{background:#8EC2F5;border-radius:5px;font-family:JetBrains Mono;font-weight:bold;}QPushButton:hover{background:#A5DEF1;}''')
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
        bgColor = '#d7d7d7'  # 文本框背景色
        bgColor = '#d7d7d7'  # 文本框背景色
        self.text_style = """QLineEdit{{ color: #4C4C4C; border-width: 1px solid black;border-radius:10px;
            padding:2px 4px; background-color: {0}; color: #000000; 
                font_family:JetBrains Mono;font-weight:bold; }} 
            QLineEdit:hover{{ border: 2px solid #d7d7d7;}}""".format(
            bgColor)

        self.select_text_style = """QComboBox{{ color: #4C4C4C; border: 0px solid black;border-radius:10px;
                   padding:2px 4px; background-color: {0}; color: #000000; 
                       font_family:JetBrains Mono;font-weight:bold; }} 
                   QComboBox:hover{{ border: 2px solid #d7d7d7;}}
                   QComboBox:drop-down {{subcontrol-origin: padding;subcontrol-position: top right;width: 30px;font_family:JetBrains Mono;font-weight:bold;}}
                   QComboBox QAbstractItemView{{height: 100px; border: 0px; border-radius:10px;background-color:#d7d7d7; color: #000000; selection-color: #000000;font_family:JetBrains Mono;font-weight:bold; 
                   selection-background-color: #A5DEF1; padding:5px, 5px,15px,15px;}}
                   QComboBox QAbstractItemView:item{{min-height: 30px; }}
                   """.format(
            bgColor)


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

    def cancel_clicked(self):
        self.close()

    def show_dialog(self):
        self.show()


class PQ_Dialog(Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(480, 300)

        self.PQ_text = [[]] * 2
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

        self.Q_label = QLabel(self)
        self.Q_label.move(100, 160)
        self.Q_label.setText('Q(var)')
        self.Q_label.setStyleSheet(self.label_style)
        self.Q_data = QLineEdit(self)
        self.Q_data.move(200, 160)
        self.Q_data.setPlaceholderText("请输入Q(var)")
        self.Q_data.setStyleSheet(self.text_style)

        self.set_button.clicked.connect(lambda: self.save_text())

    def save_text(self):
        P = 0
        Q = 0
        if self.P_data.text() != "":
            try:
                P = float(self.P_data.text())
            except ValueError:
                pass
        if self.Q_data.text() != "":
            try:
                Q = float(self.Q_data.text())
            except ValueError:
                pass
        self.PQ_text = [P, Q]
        print(self.PQ_text)
        self.close()


class PV_Dialog(Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(480, 300)

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
        P = 0
        V = 0
        if self.P_data.text() != "":
            try:
                P = float(self.P_data.text())
            except ValueError:
                pass
        if self.V_data.text() != "":
            try:
                V = float(self.V_data.text())
            except ValueError:
                pass
        self.PV_text = [P, V]
        print(self.PV_text)
        self.close()


class VA_Dialog(Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(530, 300)

        self.VA_text = [[]] * 2

        self.set_button.move(330, 250)
        self.cancel_button.move(430, 250)

        self.V_label = QLabel(self)
        self.V_label.move(100, 100)
        self.V_label.setText('V(v)')
        self.V_label.setStyleSheet(self.label_style)
        self.V_data = QLineEdit(self)
        self.V_data.move(250, 100)
        self.V_data.setPlaceholderText("请输入V(v)")
        self.V_data.setStyleSheet(self.text_style)

        self.A_label = QLabel(self)
        self.A_label.move(100, 160)
        self.A_label.setText('V的辐角(度)')
        self.A_label.setStyleSheet(self.label_style)
        self.A_data = QLineEdit(self)
        self.A_data.move(250, 160)
        self.A_data.setPlaceholderText("请输入V的辐角")
        self.A_data.setStyleSheet(self.text_style)

        self.set_button.clicked.connect(lambda: self.save_text())
        self.show()

    def save_text(self):
        V = 0
        A = 0
        if self.V_data.text() != "":
            try:
                V = float(self.V_data.text())
            except ValueError:
                pass
        if self.A_data.text() != "":
            try:
                A = float(self.A_data.text())
            except ValueError:
                pass
        self.VA_text = [V, A]
        print(self.VA_text)
        self.close()


class Wire_Dialog(Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(650, 650)

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
        # self.show()

    def selected_type(self):
        if self.type_select.highlighted():
            self.selected_type_index = self.type_select.currentIndex()
        return self.selected_type_index

    def save_text(self):
        the_type = 0
        D1 = 0
        D2 = 0
        D3 = 0
        diameter = 0
        line_dist = 0
        length = 0
        S_wire = 0

        if self.type_select.currentIndex() != "":
            try:
                the_type = float(self.type_select.currentIndex())
            except ValueError:
                pass

        if self.D1_data.text() != "":
            try:
                D1 = float(self.D1_data.text())
            except ValueError:
                pass

        if self.D2_data.text() != "":
            try:
                D2 = float(self.D2_data.text())
            except ValueError:
                pass

        if self.D3_data.text() != "":
            try:
                D3 = float(self.D3_data.text())
            except ValueError:
                pass

        if self.diameter_data.text() != "":
            try:
                diameter = float(self.diameter_data.text())
            except ValueError:
                pass

        if self.line_distance_data.text() != "":
            try:
                line_dist = float(self.line_distance_data.text())
            except ValueError:
                pass

        if self.length_data.text() != "":
            try:
                length = float(self.length_data.text())
            except ValueError:
                pass

        if self.S_wire_data.text() != "":
            try:
                S_wire = float(self.S_wire_data.text())
            except ValueError:
                pass

        # self.wire_text = [self.type_select.currentIndex(), self.D1_data.text(), self.D2_data.text(),
        #                   self.D3_data.text(),
        #                   self.diameter_data.text(),
        #                   self.line_distance_data.text(),
        #                   self.length_data.text(), self.S_wire_data.text()]
        self.wire_text = [the_type, D1, D2, D3, diameter, line_dist, length, S_wire]
        print(self.wire_text)
        self.close()


class Transformer_Dialog(Dialog):
    def __init__(self, start_index, end_index, parent=None):
        super().__init__(parent)

        self.start_index = start_index
        self.end_index = end_index

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

        self.U_start_label = QLabel(self)
        self.U_start_label.move(100, 400)
        self.U_start_label.setText('U_start(kV)')
        self.U_start_label.setStyleSheet(self.label_style)
        self.U_start_data = QLineEdit(self)
        self.U_start_data.move(200, 400)
        self.U_start_data.setPlaceholderText("请输入U_start(kV)")
        self.U_start_data.setStyleSheet(self.text_style)

        self.U_end_label = QLabel(self)
        self.U_end_label.move(100, 460)
        self.U_end_label.setText('U_end(kV)')
        self.U_end_label.setStyleSheet(self.label_style)
        self.U_end_data = QLineEdit(self)
        self.U_end_data.move(200, 460)
        self.U_end_data.setPlaceholderText("请输入U_end(kV)")
        self.U_end_data.setStyleSheet(self.text_style)

        self.set_button.clicked.connect(lambda: self.save_text())
        # self.show()

    def save_text(self):
        Sn = 0
        Pk = 0
        Uk = 0
        Po = 0
        Io = 0
        U_start = 0
        U_end = 0

        if self.Sn_data.text() != "":
            try:
                Sn = float(self.Sn_data.text())
            except ValueError:
                pass

        if self.Pk_data.text() != "":
            try:
                Pk = float(self.Pk_data.text())
            except ValueError:
                pass

        if self.Sn_data.text() != "":
            try:
                Uk = float(self.Uk_data.text())
            except ValueError:
                pass

        if self.Sn_data.text() != "":
            try:
                Po = float(self.Po_data.text())
            except ValueError:
                pass

        if self.Sn_data.text() != "":
            try:
                Io = float(self.Io_data.text())
            except ValueError:
                pass

        if self.Sn_data.text() != "":
            try:
                U_start = float(self.U_start_data.text())
            except ValueError:
                pass

        if self.Sn_data.text() != "":
            try:
                U_end = float(self.U_end_data.text())
            except ValueError:
                pass

        # Sn = float(self.Sn_data.text())
        # Pk = float(self.Pk_data.text())
        # Uk = float(self.Uk_data.text())
        # Po = float(self.Po_data.text())
        # Io = float(self.Io_data.text())
        # U_start = float(self.U_start_data.text())
        # U_end = float(self.U_end_data.text())
        if U_start > U_end:
            Uh = U_start
            Ul = U_end
            Uh_index = self.start_index
            Ul_index = self.end_index
        else:
            Uh = U_end
            Ul = U_start
            Uh_index = self.end_index
            Ul_index = self.start_index

        self.tf_text = [Sn, Pk, Uk, Po, Io, Uh, Ul, Uh_index, Ul_index]
        print(self.tf_text)
        self.close()


class File_Dialog(Dialog):
    def __init__(self, mode, parent=None):
        super().__init__(parent)
        self.Name_label = QLabel(self)
        self.Name_label.move(100, 100)
        if mode == "save":
            self.setWindowTitle('Saving File')
            self.Name_label.setText('Save in file "back_up.txt"')
        elif mode == "load":
            self.setWindowTitle('Loading File')
            self.Name_label.setText('Load in file "back_up.txt"')
        else:
            print("Error! invalid mode for file_dialog!")

        self.resize(550, 600)
        self.set_button.move(350, 550)

        self.Name_label.setStyleSheet(self.label_style)

        self.set_button.clicked.connect(self.close())
        self.show_dialog()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Wire_Dialog()
    win.show()
    # print(win.tf_text)
    sys.exit(app.exec_())
