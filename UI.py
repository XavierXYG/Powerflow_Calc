import math
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsView, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPen, QPainter, QIcon
from PyQt5.QtCore import QLine, QPointF
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QTextEdit, QLineEdit

# 图元库
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem, QGraphicsPathItem
from PyQt5.QtGui import QPixmap, QPainterPath
import random

from Edge import *
from Node import *
from Dialog import *
from Transformer import *
from Calculate_Distance import calculate_distance

from Get_Wire_Para import Admittance_wire
from Get_Admittance import get_admittance_matrix
from Newton import Newton
from Global_X import *
from Calculate_S import *
from Interface import *
from sympy import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.active = True

        self.status_bar = self.statusBar()
        self.menu_bar = self.menuBar()
        self.toolbar = self.addToolBar('Tools')

        self.initWindow()
        self.scene = GraphicScene(self)
        self.view = GraphicView(self.scene, self)
        # 有view就要有scene
        self.view.setScene(self.scene)
        # 设置view可以进行鼠标的拖拽选择
        self.view.setDragMode(self.view.RubberBandDrag)

        self.setMinimumHeight(1000)
        self.setMinimumWidth(1000)
        self.setCentralWidget(self.view)
        self.setWindowTitle("Graphics Demo")
        self.resize(1000, 1000)

        # 美化
        # 设置窗口背景
        # self.setWindowOpacity(0.9)  # 设置窗口透明度
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏所有边框
        QToolTip.setFont(QFont('JetBrain Mono', 9))

        self.pushbutton_close = QPushButton(self)
        self.pushbutton_close.setGeometry(QtCore.QRect(850, 10, 30, 30))
        self.pushbutton_close.setObjectName("pushButton")
        self.pushbutton_close.setStyleSheet('''QPushButton{background:#F28086;border-radius:15px;}
             QPushButton:hover{background:#F6BFC1;}''')
        self.pushbutton_close.setToolTip('<b>Close</b>')
        self.pushbutton_close.clicked.connect(self.close)  # 关闭窗口

        self.pushbutton_max = QPushButton(self)
        self.pushbutton_max.setGeometry(QtCore.QRect(900, 10, 30, 30))
        self.pushbutton_max.setObjectName("pushButton_max")
        self.pushbutton_max.setStyleSheet('''QPushButton{background:#FFD666;border-radius:15px;}
             QPushButton:hover{background:#F5DEB3;}''')
        self.pushbutton_max.setToolTip('<b>Larger</b>')
        self.pushbutton_max.clicked.connect(lambda: self.show_change_window())  # 最大化窗口

        self.pushbutton_mini = QPushButton(self)
        self.pushbutton_mini.setGeometry(QtCore.QRect(950, 10, 30, 30))
        self.pushbutton_mini.setObjectName("pushButton_mini")
        self.pushbutton_mini.setStyleSheet('''QPushButton{background:#8EC2F5;border-radius:15px;}
             QPushButton:hover{background:#A5DEF1;}''')
        self.pushbutton_mini.setToolTip('<b>Minimize</b>')
        self.pushbutton_mini.clicked.connect(self.showMinimized)  # 最小化窗口

    def show_change_window(self):
        desktop = QApplication.desktop()
        if self.width() < desktop.width():
            self.showMaximized()
            # self.setWindowState(Qt.WindowMaximized)
            self.pushbutton_close.move(desktop.width() - 150, 10)
            self.pushbutton_max.move(desktop.width() - 100, 10)
            self.pushbutton_mini.move(desktop.width() - 50, 10)
            self.pushbutton_max.setToolTip('<b>Smaller</b>')
        else:
            self.showNormal()
            self.pushbutton_close.move(850, 10)
            self.pushbutton_max.move(900, 10)
            self.pushbutton_mini.move(950, 10)
            self.pushbutton_max.setToolTip('<b>Larger</b>')

    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 让窗口可以移动
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

    def addFile(self):
        pass

    def openFile(self):
        self.scene.edges = []
        self.scene.nodes = []
        self.scene.clear()

        with open(str("./files/mission.txt"), "r") as f:
            lines = f.readlines()
            for i in range(len(lines)):

                if lines[i][:11] == "Node Index:":
                    temp_type = lines[i + 1][10:-1]
                    temp_item_x = float(lines[i + 2][4:-1])
                    temp_item_y = float(lines[i + 3][4:-1])
                    temp_node = Node(self.scene, temp_type, temp_item_x, temp_item_y)
                    if lines[i + 4][0] == 'V':  # VA
                        temp_node.data_dialog.V_data.setText(lines[i + 4][4:-1])
                        temp_node.data_dialog.A_data.setText(lines[i + 5][4:-1])
                    elif lines[i + 5][0] == 'Q':  # PQ
                        temp_node.data_dialog.P_data.setText(lines[i + 4][4:-1])
                        temp_node.data_dialog.Q_data.setText(lines[i + 5][4:-1])
                    elif lines[i + 5][0] == 'V':  # PV
                        temp_node.data_dialog.P_data.setText(lines[i + 4][4:-1])
                        temp_node.data_dialog.V_data.setText(lines[i + 5][4:-1])
                    else:
                        pass

                    self.scene.add_node(temp_node)
                    temp_node.data_dialog.save_text()

                elif lines[i][:11] == "Edge Index:":
                    temp_type = lines[i + 1][10:-1]
                    temp_start_x = float(lines[i + 3][4:-1])
                    temp_start_y = float(lines[i + 4][4:-1])
                    temp_start_item = self.scene.nodes[int(lines[i + 5][-2])].gr_node

                    temp_end_x = float(lines[i + 7][4:-1])
                    temp_end_y = float(lines[i + 8][4:-1])
                    temp_end_item = self.scene.nodes[int(lines[i + 9][-2])].gr_node

                    temp_edge = Edge(self.scene, temp_type, temp_start_item, temp_end_item)

                    if temp_type == "TL":
                        temp_edge.data_dialog.type_select.selectIndex = int(lines[i + 10][-2])
                        temp_edge.data_dialog.D1_data.setText(lines[i + 11][5:-1])
                        temp_edge.data_dialog.D2_data.setText(lines[i + 12][5:-1])
                        temp_edge.data_dialog.D3_data.setText(lines[i + 13][5:-1])
                        temp_edge.data_dialog.diameter_data.setText(lines[i + 14][11:-1])
                        temp_edge.data_dialog.line_distance_data.setText(lines[i + 15][16:-1])
                        temp_edge.data_dialog.length_data.setText(lines[i + 16][9:-1])
                        temp_edge.data_dialog.S_wire_data.setText(lines[i + 17][9:-1])
                    elif temp_type == "TF":
                        temp_edge.data_dialog.Sn_data.setText(lines[i + 10][5:-1])
                        temp_edge.data_dialog.Pk_data.setText(lines[i + 11][5:-1])
                        temp_edge.data_dialog.Uk_data.setText(lines[i + 12][5:-1])
                        temp_edge.data_dialog.Po_data.setText(lines[i + 13][5:-1])
                        temp_edge.data_dialog.Io_data.setText(lines[i + 14][5:-1])
                        temp_edge.data_dialog.U_start_data.setText(lines[i + 15][5:-1])
                        temp_edge.data_dialog.U_end_data.setText(lines[i + 16][5:-1])
                    else:
                        pass

                    temp_edge.data_dialog.save_text()

            f.close()
            # print(len(self.scene.edges))

    def saveFile(self):
        file_name = "back_up"
        print(file_name + ".txt")

        with open(str("./files/" + file_name + ".txt"), "w") as f:

            f.write(str("Nodes:" + "\n"))
            for node in self.scene.nodes:
                f.write(str("Node Index:" + str(node.gr_node.getNodeIndex()) + "\n"))
                f.write(str("Node Type:" + str(node.type) + "\n"))
                f.write(str("x = " + str(node.gr_node.pos().x()) + "\n"))
                f.write(str("y = " + str(node.gr_node.pos().y()) + "\n"))

                if node.type == "PQ":
                    f.write(str("P = " + str(node.data_dialog.PQ_text[0] / 1e6) + "\n"))
                    f.write(str("Q = " + str(node.data_dialog.PQ_text[1] / 1e6) + "\n"))
                elif node.type == "PV":
                    f.write(str("P = " + str(node.data_dialog.PV_text[0] / 1e6) + "\n"))
                    f.write(str("V = " + str(node.data_dialog.PV_text[1] / 1e3) + "\n"))
                elif node.type == "VTheta":
                    f.write(str("V = " + str(node.data_dialog.VA_text[0] / 1e3) + "\n"))
                    f.write(str("A = " + str(node.data_dialog.VA_text[1]) + "\n"))
                else:
                    print("Error! Saving Wrong-typed nodes!")

            f.write(str("Edges:" + "\n"))
            for edge in self.scene.edges:
                f.write(str("Edge Index:" + str(edge.gr_edge.getEdgeIndex()) + "\n"))
                f.write(str("Edge Type:" + str(edge.type) + "\n"))
                f.write(str("starting point: " + "\n"))
                f.write(str("x = " + str(edge.gr_edge.pos_src[0]) + "\n"))
                f.write(str("y = " + str(edge.gr_edge.pos_src[1]) + "\n"))
                f.write(str("start item index = " + str(edge.start_item.getNodeIndex()) + "\n"))
                f.write(str("ending point: " + "\n"))
                f.write(str("x = " + str(edge.gr_edge.pos_dst[0]) + "\n"))
                f.write(str("y = " + str(edge.gr_edge.pos_dst[1]) + "\n"))
                f.write(str("end item index = " + str(edge.end_item.getNodeIndex()) + "\n"))

                if edge.type == "TL":
                    f.write(str("type = " + str(edge.data_dialog.wire_text[0]) + "\n"))
                    f.write(str("D1 = " + str(edge.data_dialog.wire_text[1] / 1e3) + "\n"))
                    f.write(str("D2 = " + str(edge.data_dialog.wire_text[2] / 1e3) + "\n"))
                    f.write(str("D3 = " + str(edge.data_dialog.wire_text[3] / 1e3) + "\n"))
                    f.write(str("Diameter = " + str(edge.data_dialog.wire_text[4]) + "\n"))
                    f.write(str("Line Distance = " + str(edge.data_dialog.wire_text[5]) + "\n"))
                    f.write(str("Length = " + str(edge.data_dialog.wire_text[6]) + "\n"))
                    f.write(str("S_Wire = " + str(edge.data_dialog.wire_text[7]) + "\n"))
                elif edge.type == "TF":
                    f.write(str("Sn = " + str(edge.data_dialog.tf_text[0]) + "\n"))
                    f.write(str("Pk = " + str(edge.data_dialog.tf_text[1]) + "\n"))
                    f.write(str("Uk = " + str(edge.data_dialog.tf_text[2]) + "\n"))
                    f.write(str("Po = " + str(edge.data_dialog.tf_text[3]) + "\n"))
                    f.write(str("Io = " + str(edge.data_dialog.tf_text[4]) + "\n"))
                    f.write(str("Uh = " + str(edge.data_dialog.tf_text[5]) + "\n"))
                    f.write(str("Ul = " + str(edge.data_dialog.tf_text[6]) + "\n"))
                    f.write(str("hn = " + str(edge.data_dialog.tf_text[7]) + "\n"))
                    f.write(str("ln = " + str(edge.data_dialog.tf_text[8]) + "\n"))

                else:
                    print("Error! Saving Wrong-typed edges!")

            f.close()
            file_dialog = File_Dialog("save")

    def openGuide(self):
        pass

    def openAbout(self):
        pass

    def add_v_theta(self):
        self.view.selected_node_type = 'VTheta'
        self.view.addNodeHandle('VTheta')

    def add_p_q(self):
        self.view.selected_node_type = 'PQ'
        self.view.addNodeHandle('PQ')

    def add_p_v(self):
        self.view.selected_node_type = 'PV'
        self.view.addNodeHandle('PV')

    def add_transformer(self):
        self.view.selected_edge_type = 'TF'
        self.view.addEdgeHandle('TF')

    def add_line(self):
        self.view.selected_edge_type = 'TL'
        self.view.addEdgeHandle('TL')

    def initWindow(self):
        # ---- Menu Bar Actions ----
        # add
        add_file_action = QAction(QIcon('add.png'), 'Add New File...', self)
        add_file_action.setShortcut('Ctrl+N')
        add_file_action.setStatusTip('Add New File')
        add_file_action.triggered.connect(self.addFile)
        # open
        open_file_action = QAction(QIcon('open.png'), 'Open Existing File...', self)
        open_file_action.setShortcut('Ctrl+O')
        open_file_action.setStatusTip('Open Existing File')
        open_file_action.triggered.connect(self.openFile)
        # save
        save_file_action = QAction(QIcon('save.png'), 'Save File', self)
        save_file_action.setShortcut('Ctrl+S')
        save_file_action.setStatusTip('Save File')
        save_file_action.triggered.connect(self.saveFile)
        # exit
        exit_file_action = QAction(QIcon('exit.png'), 'Exit', self)
        exit_file_action.setShortcut('Ctrl+Q')
        exit_file_action.setStatusTip('Exit Application')
        exit_file_action.triggered.connect(self.close)
        # guidance
        guide_action = QAction(QIcon('guidance.png'), 'How to use', self)
        guide_action.setShortcut('Ctrl+H')
        guide_action.setStatusTip('User Guidance')
        guide_action.triggered.connect(self.openGuide)
        # about
        about_action = QAction(QIcon('about.png'), 'About...', self)
        about_action.setStatusTip('Development Information')
        about_action.triggered.connect(self.openAbout)

        # ---- Tool Bar Actions ----
        # Add_V_theta_Bus
        add_v_theta_action = QAction(QIcon('./images/v_theta.png'), 'Add V-theta Bus', self)
        add_v_theta_action.setStatusTip('Add V-theta Bus')
        add_v_theta_action.triggered.connect(self.add_v_theta)
        add_v_theta_action.setFont(QFont('JetBrain Mono', 9))
        # Add_PV_Bus
        add_p_v_action = QAction(QIcon('./images/p_v.png'), 'Add P-V Bus', self)
        add_p_v_action.setStatusTip('Add P-V Bus')
        add_p_v_action.triggered.connect(self.add_p_v)
        # Add_PQ_Bus
        add_p_q_action = QAction(QIcon('./images/p_q.png'), 'Add P-Q Bus', self)
        add_p_q_action.setStatusTip('Add P-Q Bus')
        add_p_q_action.triggered.connect(self.add_p_q)
        # Add_Transformer
        add_transformer_action = QAction(QIcon('./images/transformer.jpg'), 'Add Transformer', self)
        add_transformer_action.setStatusTip('Add Transformer')
        add_transformer_action.triggered.connect(self.add_transformer)
        # Add_Transmission_Line
        add_line_action = QAction(QIcon('./images/line.jpg'), 'Add Transmission Line', self)
        add_line_action.setStatusTip('Add Transmission Line')
        add_line_action.triggered.connect(self.add_line)
        # Calculate
        calculate_action = QAction(QIcon('./images/calculate.png'), 'Calculate Result', self)
        calculate_action.setStatusTip('Calculate Result')
        calculate_action.triggered.connect(self.calculate_result)

        # show_Powerflow
        powerflow_action = QAction(QIcon('./images/power.png'), 'Calculate Power', self)
        powerflow_action.setStatusTip('Calculate node power')
        powerflow_action.triggered.connect(self.power_show)

        # show_delta_Powerflow
        delta_powerflow_action = QAction(QIcon('./images/delta_power.png'), 'Calculate Delta Power', self)
        delta_powerflow_action.setStatusTip('Calculate delta power used by edge resistnace')
        delta_powerflow_action.triggered.connect(self.delta_power_show)

        # ---- Bar Implementation ----
        # status bar
        # self.status_bar = self.statusBar()

        # menu bar
        # self.menu_bar = self.menuBar()
        self.menu_bar.setStyleSheet('''
        QMenuBar { background-color: rgb(49,49,49); color: rgb(255,255,255);  border: 0px solid ; font_family:JetBrains Mono;font-weight:bold;padding:6px 10px; }
        QMenuBar:item { background-color: rgb(49,49,49); color: rgb(255,255,255);height: 30px}
        QMenu:item:selected{background-color:#F5DEB3; color:rgb(49,49,49);}
        QMenu:item{background-color:rgb(255,250,250); color:black; font_family:JetBrains Mono;font-weight:bold;padding:0px 0px; width: 230px;}
         ''')

        self.menu_bar.setNativeMenuBar(False)
        file_menu = self.menu_bar.addMenu('File')
        help_menu = self.menu_bar.addMenu('Help')

        # add actions to menu bar
        file_menu.addAction(add_file_action)
        file_menu.addAction(open_file_action)
        file_menu.addAction(save_file_action)
        file_menu.addAction(exit_file_action)
        help_menu.addAction(guide_action)
        help_menu.addAction(about_action)

        # tool bar
        # self.toolbar = self.addToolBar('Tools')
        self.toolbar.setStyleSheet("""
               QToolBar { background-color: rgb(49,49,49); color: rgb(255,255,255);  border: 0px solid ; }
            """)

        # add actions to tool bar
        self.toolbar.addAction(add_v_theta_action)
        self.toolbar.addAction(add_p_v_action)
        self.toolbar.addAction(add_p_q_action)
        self.toolbar.addAction(add_transformer_action)
        self.toolbar.addAction(add_line_action)
        self.toolbar.addAction(calculate_action)
        self.toolbar.addAction(powerflow_action)
        self.toolbar.addAction(delta_powerflow_action)

        # add message to status bar
        self.status_bar.showMessage('Ready')

        self.show()

    def getNodeTypeNumList(self):
        self.PQ_nodes = []
        self.PV_nodes = []
        self.VTheta_nodes = []
        for node in self.scene.nodes:
            if node.type == "PQ":
                self.PQ_nodes.append(node)
            elif node.type == "PV":
                self.PV_nodes.append(node)
            elif node.type == "VTheta":
                self.VTheta_nodes.append(node)
            else:
                print("Error! Getting wrong node number.")

        return [len(self.PQ_nodes), len(self.PV_nodes), len(self.VTheta_nodes)]

    def getNodeSum(self):
        return 2 * sum(self.getNodeTypeNumList())

    def getGlobal_Y(self):
        self.global_Y = []

        for PQ_node in self.PQ_nodes:
            self.global_Y.append(PQ_node.data_dialog.PQ_text)
        for PV_node in self.PV_nodes:
            self.global_Y.append(PV_node.data_dialog.PV_text)
        for VTheta_node in self.VTheta_nodes:
            self.global_Y.append(VTheta_node.data_dialog.VA_text)

        print(self.global_Y)
        return self.global_Y

    def getTransformers(self):
        tf_list = []
        for edge in self.scene.edges:
            if edge.type == "TF":
                tf = Transformer(edge.data_dialog.tf_text[0], edge.data_dialog.tf_text[1], edge.data_dialog.tf_text[2],
                                 edge.data_dialog.tf_text[3], edge.data_dialog.tf_text[4], edge.data_dialog.tf_text[5],
                                 edge.data_dialog.tf_text[6], edge.data_dialog.tf_text[7], edge.data_dialog.tf_text[8])
                tf_list.append(tf)
        return tf_list

    def calculate_result(self):
        run_algorithm(self)

    def power_show(self):
        power_real_show(self)

    def delta_power_show(self):
        delta_power_real_show(self)


class GraphicScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 一些关于网格背景的设置
        self.grid_size = 20  # 一块网格的大小 （正方形的）
        self.grid_squares = 5  # 网格中正方形的区域个数

        # 一些颜色
        self._color_background = QColor('#393939')
        self._color_light = QColor('#2f2f2f')
        self._color_dark = QColor('#292929')
        # 一些画笔
        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)

        # 设置画背景的画笔
        self.setBackgroundBrush(self._color_background)
        self.setSceneRect(0, 0, 1000, 1000)

        self.nodes = []  # 存储节点
        self.edges = []  # 存储连线

    def add_node(self, node):
        self.nodes.append(node)
        self.addItem(node.gr_node)

    def remove_node(self, node):
        self.nodes.remove(node)
        # 删除图元时，遍历与其连接的线，并移除
        for edge in self.edges[:]:
            if edge.start_item is node.gr_node or edge.end_item is node.gr_node:
                self.remove_edge(edge)
        self.removeItem(node.gr_node)

    def add_edge(self, edge):
        self.edges.append(edge)
        self.addItem(edge.gr_edge)
        # self.edges = sorted(set(self.edges), key=self.edges.index)  # 删除重复项

    def remove_edge(self, edge):
        self.edges.remove(edge)
        self.removeItem(edge.gr_edge)
        # self.edges = sorted(set(self.edges), key=self.edges.index)

    # override
    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # 获取背景矩形的上下左右的长度，分别向上或向下取整数
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        # 从左边和上边开始
        first_left = left - (left % self.grid_size)  # 减去余数，保证可以被网格大小整除
        first_top = top - (top % self.grid_size)

        # 分别收集明、暗线
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.grid_size):
            if x % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.grid_size):
            if y % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))

        # 最后把收集的明、暗线分别画出来
        painter.setPen(self._pen_light)
        if lines_light:
            painter.drawLines(*lines_light)

        painter.setPen(self._pen_dark)
        if lines_dark:
            painter.drawLines(*lines_dark)


class GraphicView(QGraphicsView):
    def __init__(self, graphic_scene, parent=None):
        super().__init__(parent)

        self.gr_scene = graphic_scene  # 将scene传入此处托管，方便在view中维护
        self.parent = parent

        self.edge_enable = False  # 用来记录目前是否可以画线条
        self.enabled_edge_type = "TL"  # TL or TF
        self.drag_edge = None  # 记录拖拽时的线
        self.selected_item_index = 0  # 记录当前被选中的图元的index
        self.selected_edge_index = 0  # 记录当前被选中的edge的index
        self.selected_node_type = ''  # 结点的类型
        self.selected_edge_type = ''  # edge的类型

        self.init_ui()

    def init_ui(self):
        self.setScene(self.gr_scene)
        # 设置渲染属性
        self.setRenderHints(QPainter.Antialiasing |  # 抗锯齿
                            QPainter.HighQualityAntialiasing |  # 高品质抗锯齿
                            QPainter.TextAntialiasing |  # 文字抗锯齿
                            QPainter.SmoothPixmapTransform |  # 使图元变换更加平滑
                            QPainter.LosslessImageRendering)  # 不失真的图片渲染
        # 视窗更新模式
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        # 设置水平和竖直方向的滚动条不显示
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(self.AnchorUnderMouse)
        # 设置拖拽模式
        self.setDragMode(self.RubberBandDrag)

    # ---- Node & Edge Handlers ----
    def addNodeHandle(self, nd_type):
        # gr_item = GraphicItem(nd_type)
        # gr_item.setPos(500, 500)
        # self.gr_scene.add_node(gr_item)
        new_node = Node(self.scene, nd_type)
        # new_node.gr_node.setPos(500, 500)
        self.gr_scene.add_node(new_node)

    def addEdgeHandle(self, eg_type):
        self.edge_enable = True
        self.enabled_edge_type = eg_type

    # override
    def keyPressEvent(self, event):
        pass
        # # 当按下N键时，会在scene的（0,0）位置出现此图元
        # if event.key() == Qt.Key_N:
        #     self.addNodeHandle('VTheta')
        #
        # # 当按下E键时，启动线条功能，再次按下则是关闭
        # if event.key() == Qt.Key_E:
        #     self.addEdgeHandle('TL')
        #
        # if event.key() == Qt.Key_Escape:
        #     self.edge_enable = False

    # override
    def mousePressEvent(self, event):
        item = self.get_item_at_click(event)
        if event.button() == Qt.RightButton:  # 判断鼠标右键点击
            if isinstance(item, GraphicItem):
                self.gr_scene.remove_node(item.getNodeWrap())
        elif self.edge_enable:
            if isinstance(item, GraphicItem):  # 判断点击对象是否为图元的实例, 确认起点是图元后，开始拖拽
                self.edge_drag_start(self.enabled_edge_type, item)
        else:
            # 如果写到最开头，则线条拖拽功能会不起作用
            super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        item = self.get_item_at_click(event)
        if isinstance(item, GraphicItem):
            self.selected_item_index = item.getNodeIndex()
            print(self.selected_item_index)
            selected_node = item.getNodeWrap()
            selected_node.data_dialog.show_dialog()
        else:
            edge = self.get_edge_at_click(event)
            if isinstance(edge.gr_edge, GraphicEdge):
                self.selected_edge_index = edge.gr_edge.getEdgeIndex()
                print(self.selected_edge_index)
                edge.data_dialog.show_dialog()

    def mouseReleaseEvent(self, event):
        if self.edge_enable:
            # 拖拽结束后，关闭此功能
            self.edge_enable = False
            item = self.get_item_at_click(event)
            # 终点图元不能是起点图元，即无环图
            if isinstance(item, GraphicItem) and item is not self.drag_start_item:
                self.edge_drag_end(self.enabled_edge_type, item)
            elif item is None:
                pass
            else:
                self.drag_edge.remove()
                self.drag_edge = None
        else:
            super().mouseReleaseEvent(event)

    # override
    def mouseMoveEvent(self, event):
        # 实时更新线条
        pos = event.pos()
        if self.edge_enable and self.drag_edge is not None:
            sc_pos = self.mapToScene(pos)
            self.drag_edge.gr_edge.set_dst(sc_pos.x(), sc_pos.y())
            self.drag_edge.gr_edge.update()
        super().mouseMoveEvent(event)

    def get_item_at_click(self, event):
        """ 获取点击位置的图元，无则返回None. """
        pos = event.pos()
        item = self.itemAt(pos)
        return item

    def get_items_at_rubber_select(self, event):
        """ 返回一个所有选中图元的列表，对此操作即可 """
        area = self.rubberBandRect()
        return self.items(area)

    def get_edge_at_click(self, event):
        """ 获取点击位置的Edge，无则返回None. """
        sc_pos = self.mapToScene(event.pos())
        pos = [sc_pos.x(), sc_pos.y()]
        distance = []
        for edge in self.gr_scene.edges:
            distance_element = calculate_distance(edge.gr_edge.pos_src, edge.gr_edge.pos_dst, pos)
            distance.append(distance_element)
            # print(edge.pos_src, edge.pos_dst)
        if len(distance):
            min_value = min(distance)
            if min_value <= 10:
                result_edge = self.gr_scene.edges[distance.index(min_value)]
            else:
                result_edge = None
        else:
            result_edge = None
        return result_edge

    def edge_drag_start(self, eg_type, item):
        self.drag_start_item = item
        self.drag_edge = Edge(self.gr_scene, eg_type, self.drag_start_item, None)  # 开始拖拽线条，注意到拖拽终点为None

    def edge_drag_end(self, eg_type, item):
        new_edge = Edge(self.gr_scene, eg_type, self.drag_start_item, item)  # 拖拽结束
        self.drag_edge.remove()  # 删除拖拽时画的线
        self.drag_edge = None
        # new_edge.store()  # 保存最终产生的连接线


# class GraphicItem(QGraphicsPixmapItem):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.pix = QPixmap("./images/icon.jpg")
#         self.width = 100  # 图元宽
#         self.height = 100  # 图元高
#         self.setPixmap(self.pix)  # 设置图元
#         self.setFlag(QGraphicsItem.ItemIsSelectable)  # ***设置图元是可以被选择的
#         self.setFlag(QGraphicsItem.ItemIsMovable)  # ***设置图元是可以被移动的
#
#     def mouseMoveEvent(self, event):
#         super().mouseMoveEvent(event)
#         # 如果图元被选中，就更新连线，这里更新的是所有。可以优化，只更新连接在图元上的。
#         if self.isSelected():
#             for gr_edge in self.scene().edges:
#                 gr_edge.edge_wrap.update_positions()
#
#     def getNodeIndex(self):
#         return self.scene().nodes.index(self)

def power_real_show(demo):
    dict_S, dict_delta_S = run_algorithm(demo)
    power_show = Power_Dialog(dict_S)


def delta_power_real_show(demo):
    dict_S, dict_delta_S = run_algorithm(demo)
    delta_power_show = Power_Dialog(dict_delta_S)


def run_algorithm(demo):
    print("0")
    temp_Topology = Admittance_wire(demo.scene.nodes, demo.scene)
    print(temp_Topology)

    print("1")
    transformer_list = demo.getTransformers()
    print(transformer_list)

    print("2")
    network_1 = Network(temp_Topology, transformer_list)
    print(network_1)

    print("3")
    Topology = network_1.transform()
    print(Topology)

    print("4")
    y_admittance = get_admittance_matrix(Topology)
    print(y_admittance)

    print("5")
    factor = 220
    if len(network_1.tfs_):
        factor = network_1.U_init() - random.random()
    else:
        for node in demo.scene.nodes:
            if node.type == "VTheta":
                factor = node.data_dialog.VA_text[0]
                break
    print(factor)
    print("6")
    node_sum = demo.getNodeSum()
    bus_num = demo.getNodeTypeNumList()
    global_Y = demo.getGlobal_Y()

    print(node_sum)
    print(bus_num)
    print(global_Y)

    x = np.ones(node_sum, dtype=float) * factor
    accuracy = 5
    eqs, input_array = Interface(x, global_Y, bus_num, y_admittance)
    print("Newton: \n")
    result = nsolve(eqs, input_array, np.ones(len(input_array)) * factor)
    print(result)

    print("7")
    print("Power Flow: \n")
    S_Topology, delta_S_Topology = power_flow(result, y_admittance, demo.scene.nodes, demo.scene)
    dict_S, dict_delta_S = adjust_Power_flow_Data(S_Topology, delta_S_Topology)
    print(dict_S)
    print(dict_delta_S)
    return dict_S, dict_delta_S


def demo_run():
    app = QApplication(sys.argv)
    demo = MainWindow()
    # 适配 Retina 显示屏（选写）.
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    # ----------------------------------
    demo.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    demo_run()
