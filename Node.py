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
from Dialog import *


class Node:
    def __init__(self, scene, nd_type, x=500, y=500):
        # super().__init__()
        self.scene = scene
        self.type = nd_type
        self.gr_node = GraphicItem(self)
        self.gr_node.setPos(x, y)
        if nd_type == "PQ":
            self.data_dialog = PQ_Dialog()
        elif nd_type == "PV":
            self.data_dialog = PV_Dialog()
        elif nd_type == "VTheta":
            self.data_dialog = VA_Dialog()
        else:
            pass
        self.data_dialog.show_dialog()


class GraphicItem(QGraphicsPixmapItem):
    def __init__(self, node_wrap, parent=None):
        super().__init__(parent)
        self.type = node_wrap.type
        self.node_wrap = node_wrap
        nd_type = self.type
        self.pix = QPixmap("./icon.jpg")
        if nd_type == "PQ":
            self.pix = QPixmap("./images/p_q.png")
        elif nd_type == "PV":
            self.pix = QPixmap("./images/p_v.png")
        elif nd_type == "VTheta":
            self.pix = QPixmap("./images/v_theta.png")
        else:
            pass
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
        return self.scene().nodes.index(self.node_wrap)


# class Graphic_PQ(GraphicItem):
#     def __init__(self, P, Q, parent=None):
#         super().__init__(parent)
#         self.pix = QPixmap("./PQ_Bus.jpg")
#         self.type = "PQ"
#
#
#
# class Graphic_PV(GraphicItem):
#     def __init__(self, P, V, parent=None):
#         super().__init__(parent)
#         self.pix = QPixmap("./PV_Bus.jpg")
#         self.P = P
#         self.V = V
#         self.type = "PV"
#
#     def set_param(self, P, V):
#         self.P = P
#         self.V = V
#
#
# class Graphic_VTheta(GraphicItem):
#     def __init__(self, V, theta, parent=None):
#         super().__init__(parent)
#         self.pix = QPixmap("./PV_Bus.jpg")
#         self.V = V
#         self.theta = theta
#         self.type = "VTheta"
#
#     def set_param(self, V, theta):
#         self.V = V
#         self.theta = theta
