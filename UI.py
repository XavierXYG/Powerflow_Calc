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

from Edge import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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

        self.initWindow()

    def addFile(self):
        pass

    def openFile(self):
        pass

    def saveFile(self):
        pass

    def openGuide(self):
        pass

    def openAbout(self):
        pass

    def add_v_theta(self):
        self.view.selected_node_type = 'VTheta'
        self.view.addNodeHandle()

    def add_p_q(self):
        self.view.selected_node_type = 'PQ'

    def add_p_v(self):
        self.view.selected_node_type = 'PV'

    def add_transformer(self):
        self.view.selected_edge_type = 'transformer'

    def add_line(self):
        self.view.selected_edge_type = 'wire'
        self.view.addEdgeHandle()

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
        add_v_theta_action = QAction(QIcon('v_theta.png'), 'Add V-theta Bus', self)
        add_v_theta_action.setStatusTip('Add V-theta Bus')
        add_v_theta_action.triggered.connect(self.add_v_theta)
        # Add_PV_Bus
        add_p_v_action = QAction(QIcon('p_v.png'), 'Add P-V Bus', self)
        add_p_v_action.setStatusTip('Add P-V Bus')
        add_p_v_action.triggered.connect(self.add_p_v)
        # Add_PQ_Bus
        add_p_q_action = QAction(QIcon('p_q.png'), 'Add P-Q Bus', self)
        add_p_q_action.setStatusTip('Add P-Q Bus')
        add_p_q_action.triggered.connect(self.add_p_q)
        # Add_Transformer
        add_transformer_action = QAction(QIcon('transformer.png'), 'Add Transformer', self)
        add_transformer_action.setStatusTip('Add Transformer')
        add_transformer_action.triggered.connect(self.add_transformer)
        # Add_Transmission_Line
        add_line_action = QAction(QIcon('line.png'), 'Add Transmission Line', self)
        add_line_action.setStatusTip('Add Transmission Line')
        add_line_action.triggered.connect(self.add_line)

        # ---- Bar Implementation ----
        # status bar
        status_bar = self.statusBar()

        # menu bar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        file_menu = menu_bar.addMenu('File')
        help_menu = menu_bar.addMenu('Help')

        # add actions to menu bar
        file_menu.addAction(add_file_action)
        file_menu.addAction(open_file_action)
        file_menu.addAction(save_file_action)
        file_menu.addAction(exit_file_action)
        help_menu.addAction(guide_action)
        help_menu.addAction(about_action)

        # tool bar
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(add_v_theta_action)
        toolbar.addAction(add_p_v_action)
        toolbar.addAction(add_p_q_action)
        toolbar.addAction(add_transformer_action)
        toolbar.addAction(add_line_action)

        # add actions to tool bar

        # add message to status bar
        status_bar.showMessage('Ready')

        self.show()
        pass


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
        self.setSceneRect(0, 0, 500, 500)

        self.nodes = []  # 存储图元
        self.dataflow_nodes = []  # 存储节点数据
        self.edges = []  # 存储连线
        self.dataflow_edges = []  # 存储连线数据

    def add_node(self, node):
        self.nodes.append(node)
        self.addItem(node)

    def remove_node(self, node):
        self.nodes.remove(node)
        # 删除图元时，遍历与其连接的线，并移除
        for edge in self.edges:
            if edge.edge_wrap.start_item is node or edge.edge_wrap.end_item is node:
                self.remove_edge(edge)
        self.removeItem(node)

    def add_edge(self, edge):
        self.edges.append(edge)
        self.addItem(edge)

    def remove_edge(self, edge):
        self.edges.remove(edge)
        self.removeItem(edge)

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
    def addNodeHandle(self):
        gr_item = GraphicItem()
        gr_item.setPos(0, 0)
        self.gr_scene.add_node(gr_item)

    def addEdgeHandle(self):
        self.edge_enable = ~self.edge_enable

    # override
    def keyPressEvent(self, event):
        # 当按下N键时，会在scene的（0,0）位置出现此图元
        if event.key() == Qt.Key_N:
            self.addNodeHandle()

        # 当按下E键时，启动线条功能，再次按下则是关闭
        if event.key() == Qt.Key_E:
            self.addEdgeHandle()

        if event.key() == Qt.Key_Escape:
            self.edge_enable = False

    # override
    def mousePressEvent(self, event):
        item = self.get_item_at_click(event)
        if event.button() == Qt.RightButton:  # 判断鼠标右键点击
            if isinstance(item, GraphicItem):
                self.gr_scene.remove_node(item)
        elif self.edge_enable:
            if isinstance(item, GraphicItem):  # 判断点击对象是否为图元的实例, 确认起点是图元后，开始拖拽
                self.edge_drag_start(item)
        else:
            # 如果写到最开头，则线条拖拽功能会不起作用
            super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        item = self.get_item_at_click(event)
        if isinstance(item, GraphicItem):
            self.selected_item_index = item.getNodeIndex()
            print(self.selected_item_index)
            dialog = QWidget()
            dialog.show()
        if isinstance(item, GraphicEdge):
            self.selected_edge_index = item.getEdgeIndex()
            print(self.selected_item_index)

    def mouseReleaseEvent(self, event):
        if self.edge_enable:
            # 拖拽结束后，关闭此功能
            self.edge_enable = False
            item = self.get_item_at_click(event)
            # 终点图元不能是起点图元，即无环图
            if isinstance(item, GraphicItem) and item is not self.drag_start_item:
                self.edge_drag_end(item)
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

    def get_items_at_rubber_select(self):
        """ 返回一个所有选中图元的列表，对此操作即可 """
        area = self.rubberBandRect()
        return self.items(area)

    def edge_drag_start(self, item):
        self.drag_start_item = item
        self.drag_edge = Edge(self.gr_scene, self.drag_start_item, None)  # 开始拖拽线条，注意到拖拽终点为None

    def edge_drag_end(self, item):
        new_edge = Edge(self.gr_scene, self.drag_start_item, item)  # 拖拽结束
        self.drag_edge.remove()  # 删除拖拽时画的线
        self.drag_edge = None
        new_edge.store()  # 保存最终产生的连接线


class GraphicItem(QGraphicsPixmapItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pix = QPixmap("./icon.jpg")
        self.width = 100  # 图元宽
        self.height = 100  # 图元高
        self.setPixmap(self.pix)  # 设置图元
        self.setFlag(QGraphicsItem.ItemIsSelectable)  # ***设置图元是可以被选择的
        self.setFlag(QGraphicsItem.ItemIsMovable)  # ***设置图元是可以被移动的

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # 如果图元被选中，就更新连线，这里更新的是所有。可以优化，只更新连接在图元上的。
        if self.isSelected():
            for gr_edge in self.scene().edges:
                gr_edge.edge_wrap.update_positions()

    def getNodeIndex(self):
        return self.scene().nodes.index(self)



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
