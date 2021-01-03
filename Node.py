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


class GraphicItem(QGraphicsPixmapItem):
    def __init__(self, parent=None):
        super().__init__(parent)
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


class PQ_Bus(GraphicItem):
    def __init__(self, P, Q, parent=None):
        super().__init__(parent)
        self.pix = QPixmap("./PQ_Bus.jpg")
        self.P = P
        self.Q = Q

    def set_param(self, P, Q):
        self.P = P
        self.Q = Q


class PV_Bus(GraphicItem):
    def __init__(self, P, V, parent=None):
        super().__init__(parent)
        self.pix = QPixmap("./PV_Bus.jpg")
        self.P = P
        self.V = V

    def set_param(self, P, V):
        self.P = P
        self.V = V


class V_theta_Bus(GraphicItem):
    def __init__(self, V, theta, parent=None):
        super().__init__(parent)
        self.pix = QPixmap("./PV_Bus.jpg")
        self.V = V
        self.theta = theta

    def set_param(self, V, theta):
        self.V = V
        self.theta = theta
