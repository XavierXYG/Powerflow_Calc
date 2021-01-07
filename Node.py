from PyQt5.QtGui import QPixmap
from UI import GraphicItem, QGraphicsScene


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
