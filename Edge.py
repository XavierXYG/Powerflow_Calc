import math
import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QColor, QPen, QPainter
from PyQt5.QtCore import QLine, QPointF
# 图元库
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem, QGraphicsPathItem
from PyQt5.QtGui import QPixmap, QPainterPath
from dialog import *




class Edge(Dialog):
    def __init__(self, scene, start_item, end_item):
        # 参数分别为场景、开始图元、结束图元
        super().__init__()
        self.scene = scene
        self.start_item = start_item
        self.end_item = end_item

        # 线条图形在此处创建
        self.gr_edge = GraphicEdge(self)
        # 此类一旦被初始化就在添加进scene
        self.scene.add_edge(self.gr_edge)

        self.new_dialog = Dialog()
        self.window_show = 0


        # 开始更新
        if self.start_item is not None:
            self.update_positions()


    def add_dialog(self, dialog):
        self.dialog_dataflow.append(dialog)
        dialog.show_dialog()

    # 最终保存进scene
    def store(self):
        #add show_window_edge
        self.scene.add_edge(self.gr_edge)
        self.window_show = 1
        if self.window_show:
            self.add_dialog(self.new_dialog)
        #add show_window_edge


    # 更新位置
    def update_positions(self):
        # src_pos 记录的是开始图元的位置，此位置为图元的左上角
        src_pos = self.start_item.pos()
        # 想让线条从图元的中心位置开始，让他们都加上偏移
        patch = self.start_item.width / 2
        self.gr_edge.set_src(src_pos.x() + patch, src_pos.y() + patch)
        # 如果结束位置图元也存在，则做同样操作
        if self.end_item is not None:
            end_pos = self.end_item.pos()
            self.gr_edge.set_dst(end_pos.x() + patch, end_pos.y() + patch)
        else:
            self.gr_edge.set_dst(src_pos.x() + patch, src_pos.y() + patch)
        self.gr_edge.update()

    def remove_from_current_items(self):
        self.end_item = None
        self.start_item = None

    # 移除线条
    def remove(self):
        self.remove_from_current_items()
        self.scene.remove_edge(self.gr_edge)
        self.gr_edge = None


class GraphicEdge(QGraphicsPathItem):
    def __init__(self, edge_wrap, parent=None):
        super().__init__(parent)
        # 这个参数是GraphicEdge的包装类，见下文
        self.edge_wrap = edge_wrap
        self.width = 3.0  # 线条的宽度
        self.pos_src = [0, 0]  # 线条起始位置 x，y坐标
        self.pos_dst = [0, 0]  # 线条结束位置

        self._pen = QPen(QColor("#000"))  # 画线条的
        self._pen.setWidthF(self.width)

        self._pen_dragging = QPen(QColor("#000"))  # 画拖拽线条时线条的
        self._pen_dragging.setStyle(Qt.DashDotLine)
        self._pen_dragging.setWidthF(self.width)

        self.setFlag(QGraphicsItem.ItemIsSelectable)  # 线条可选
        self.setZValue(-1)  # 让线条出现在所有图元的最下层

    def set_src(self, x, y):
        self.pos_src = [x, y]

    def set_dst(self, x, y):
        self.pos_dst = [x, y]

    # 计算线条的路径
    def calc_path(self):
        path = QPainterPath(QPointF(self.pos_src[0], self.pos_src[1]))  # 起点
        path.lineTo(self.pos_dst[0], self.pos_dst[1])  # 终点
        return path

    # override
    def boundingRect(self):
        return self.shape().boundingRect()

    # override
    def shape(self):
        return self.calc_path()

    # override
    def paint(self, painter, graphics_item, widget=None):
        self.setPath(self.calc_path())  # 设置路径
        path = self.path()
        if self.edge_wrap.end_item is None:
            # 包装类中存储了线条开始和结束位置的图元
            # 刚开始拖拽线条时，并没有结束位置的图元，所以是None
            # 这个线条画的是拖拽路径，点线
            painter.setPen(self._pen_dragging)
            painter.drawPath(path)
        else:
            # 这画的才是连接后的线
            painter.setPen(self._pen)
            painter.drawPath(path)


class QT_wire(Edge):
    def __init__(self, stored_data):    #sequence type=1, Dm=0, diameter=0, line_distance=0, length=0, S_wire=0
        super().__init__()
        self.stored_data = stored_data
        self.pix = QPixmap("./QT_wire.jpg")



    def remove(self):
        self.stored_data.clear()

    def push_data(self):
        pass



class QT_transformer(Edge):
    def __init__(self, stored_data):   # sequence Sn=0, Pk=0, Uk=0, Po=0, Io=0, Uh=0, Ul=0
        super().__init__()
        self.stored_data = stored_data
        self.pix = QPixmap("./QT_transformer.jpg")

        self.new_transformer_dialog = Transformer_Dialog(self.new_dialog)

    def add_dialog(self, transformer_dialog):
        self.dialog_dataflow.append(transformer_dialog)
        transformer_dialog.show_dialog()

    # 最终保存进scene
    def store(self):
        self.scene.add_edge(self.gr_edge)
        self.window_show = 1
        if self.window_show:
            self.add_dialog(self.new_transformer_dialog)
        #add show_window_edge


    def remove(self):
        self.stored_data.clear()




