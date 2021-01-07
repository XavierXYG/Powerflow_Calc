from sympy import Matrix, lambdify, exp
import numpy as np
from Global_X import Global_X
from U_Coefficient import *
import math

admittance_matrix =  np.array([[1 + 2j, 2 + 3j, 1 + 1j],
                     [3 + 0j, 4 + 5j, 5],
                     [1 + 0j, 2 + 0j, 3 + 0j]])
Global_Y = np.array([[10,20],[10,50000], [242000,0]])
BusNum = [1, 1, 1]


def Interface(input):  # 输入为三个表达式向量
    PQ_bus = PQ_ef_coefficient(admittance_matrix,  Global_Y, BusNum)
    PV_bus = PV_ef_coefficient(admittance_matrix,  Global_Y, BusNum)
    VA_bus = VA_ef_coefficient(Global_Y, BusNum)
    num_PV = PV_bus.shape[1]
    num_PQ = PQ_bus.shape[1]
    num_VA = 1 * 2
    num_total_bus = num_PV + num_PQ + num_VA
    tuple_PV, tuple_PQ, tuple_VA = (), (), ()
    for i in range(num_total_bus):
        tuple_PQ = tuple_PQ + (Global_X[i],)  # 得到初始化的元组
    for j in range(num_total_bus):
        tuple_PV = tuple_PV + (Global_X[j],)  # 得到初始化的元组
    for c in range(num_total_bus):
        tuple_VA = tuple_VA + (Global_X[c],)  # 得到初始化的元组

    PV_trans = lambdify(tuple_PV, PV_bus, 'numpy')
    PQ_trans = lambdify(tuple_PQ, PQ_bus, 'numpy')
    VA_trans = lambdify(tuple_VA, VA_bus, 'numpy')

    initial_value_PV = input[:,np.newaxis]  # 变量向量赋值的接口
    initial_value_PQ = input[:,np.newaxis]
    initial_value_VA = input[:,np.newaxis]

    PV_input_tuple, PQ_input_tuple, VA_input_tuple = (), (), ()
    for c1 in range(num_total_bus):
        PV_input_tuple = PV_input_tuple + (initial_value_PV[c1],)  # 得到初始化的元组
    for c2 in range(num_total_bus):
        PQ_input_tuple = PQ_input_tuple + (initial_value_PQ[c2],)
    for c3 in range(num_total_bus):
        VA_input_tuple = VA_input_tuple + (initial_value_VA[c3],)

    result_PV = PV_trans(*PV_input_tuple)  # 给变量赋值，将表达式矩阵转化为numpy格式
    result_PQ = PQ_trans(*PQ_input_tuple)
    result_VA = VA_trans(*VA_input_tuple)
    result = np.r_[result_PQ[0], result_PV[0], result_VA[0]]
    return result


'''
if __name__ == "__main__":
    A1 = Matrix([[Global_X[1], Global_X[2], Global_X[3]**2, Global_X[1]]])
    A2 = Matrix([[Global_X[4] + Global_X[5], Global_X[5]]])
    A3 = Matrix([[Global_X[6], Global_X[7]]])
    print(A1, A2, A3)
    test = Interface(A1, A2, A3)
    print(test)
    print(GetBusNum(A1, A2, A3))
'''