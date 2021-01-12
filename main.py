# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
# Use a breakpoint in the code line below to debug your script.
# print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
# print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


# class transformer:
#     def __init__(self):
#         pass
#
#     def get_transformer(Un, Sn, Pk, Uk, Io, Po, ratio):  # Un,Sn,Pk,Uk%,Io%,Po,ratio
#         pass

from Get_Wire_Para import Admittance_wire
from UI import *
from Transformer import *
from Get_Admittance import get_admittance_matrix
from Newton import Newton
from Global_X import *
from Calculate_S import power_flow


# 定义全局变量Topology=[[]]

# global_Y=list() #global_Y 用做牛顿迭代法中的Y=F(X)

class BUS_PQ:
    def __init__(self, P, Q, position):
        pass


class BUS_PV:
    def __init__(self, P, V, position):
        pass


class BUS_Vtheta:
    def __init__(self, V, theta, position):
        pass


# type 1:cu+n=1+S=300mm2
# def get_wire(type, Da, Db, Dc, diameter, line_distance, length, S_wire):#(材料，股数)，Dm，导线直径，分裂线距离，导线长度, 导体横截面积
# pass

'''
def get_transformer(Un,Sn,Pk,Uk,Io,Po,ratio):#Un,Sn,Pk,Uk%,Io%,Po,ratio
    pass

def transform(Topology,*args ):#变压器的权重为负，
    pass

def get_admittance_matrix(Topology):
    pass

def calculate_F(admittance_matrix,*args):
    pass

def calculate_global_Y(*args):
    pass

#def Newton_iteration(global_Y, F, accuracy):  # global_Y=F(X)，非线性方程
#   pass

def Newton(x, num, accuracy): #x是初始e、f给的值，需要初始化为1
    pass

def calculate_S():
    pass
'''
if __name__ == "__main__":

    # demo run
    app = QApplication(sys.argv)
    demo = MainWindow()
    # 适配 Retina 显示屏（选写）.
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    # ----------------------------------
    demo.show()

    # Admittance
    # size_n = len(demo.scene.nodes)
    # size_n=3
    # Admittance_bus(size_n, type=4, Da=8,Db=8,Dc=16, diameter=33.6, line_distance=0, length=20, S_wire=630)
    temp_Topology = Admittance_wire(demo.scene.nodes, demo.scene)

    # Transformer
    # tf1 = Transformer(400, 500, 5, 100, 2, 231, 121, 1, 2)
    # tf2 = Transformer(400, 500, 5, 100, 2, 231, 110, 4, 3)

    transformer_list = demo.getTransformers()
    network_1 = Network(temp_Topology, transformer_list)
    Topology = network_1.transform()

    y_admittance = get_admittance_matrix(Topology)

    factor = 220000
    if len(network_1.tfs_):
        factor = network_1.U_init()
    else:
        for node in demo.scene.nodes:
            if node.type == "VTheta":
                factor = node.data_dialog.VA_text[0]
                break

    node_sum = demo.getNodeSum()
    bus_num = demo.getNodeTypeNumList()
    global_Y = demo.getGlobal_Y()
    x = np.ones(bus_num, dtype=float) * factor
    accuracy = 1e-6
    result = Newton(x, node_sum, accuracy, global_Y, bus_num, y_admittance)
    print("Newton: \n")
    print(result)

    # 有电压以后算功率流
    print("Power Flow: \n")
    print(power_flow(result, y_admittance))

    sys.exit(app.exec_())
