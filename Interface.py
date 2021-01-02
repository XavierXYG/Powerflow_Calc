from sympy import Matrix, lambdify
import numpy as np
from Global_X import Global_X


def Interface(PQ_bus, PV_bus, VA_bus):  # 输入为三个表达式向量
    num_PV = PV_bus.shape[1]
    num_PQ = PQ_bus.shape[1]
    num_VA = 1 * 2
    tuple_PV, tuple_PQ, tuple_VA = (), (), ()
    for i in range(num_PQ):
        tuple_PQ = tuple_PQ + (Global_X[i],)  # 得到初始化的元组
    print(tuple_PQ)
    for j in range(num_PQ, num_PQ + num_PV):
        tuple_PV = tuple_PV + (Global_X[j],)  # 得到初始化的元组
    print(tuple_PV)
    start_range, end_range = num_PQ + num_PV, num_PQ + num_PV + num_VA
    for c in range(start_range, end_range):
        tuple_VA = tuple_VA + (Global_X[c],)  # 得到初始化的元组
    print(tuple_VA)

    PV_trans = lambdify(tuple_PV, PV_bus, 'numpy')
    PQ_trans = lambdify(tuple_PQ, PQ_bus, 'numpy')
    VA_trans = lambdify(tuple_VA, VA_bus, 'numpy')

    initial_value_PV = np.random.rand(num_PV, 1)  # 变量向量赋值的接口
    initial_value_PQ = np.random.rand(num_PQ, 1)
    initial_value_VA = np.random.rand(num_VA, 1)

    PV_input_tuple, PQ_input_tuple, VA_input_tuple = (), (), ()
    for c1 in range(num_PV):
        PV_input_tuple = PV_input_tuple + (initial_value_PV[c1],)  # 得到初始化的元组
    for c2 in range(num_PQ):
        PQ_input_tuple = PQ_input_tuple + (initial_value_PQ[c2],)
    for c3 in range(num_VA):
        VA_input_tuple = VA_input_tuple + (initial_value_VA[c3],)

    result_PV = PV_trans(*PV_input_tuple)  # 给变量赋值，将表达式矩阵转化为numpy格式
    result_PQ = PQ_trans(*PQ_input_tuple)
    result_VA = VA_trans(*VA_input_tuple)
    result = np.r_[result_PQ[0], result_PV[0], result_VA[0]]
    return result


def GetBusNum(PQ_bus, PV_bus, VA_bus):
    num_PV = PV_bus.shape[1]
    num_PQ = PQ_bus.shape[1]
    num_VA = 1 * 2
    return [num_PQ, num_PV, num_VA]


if __name__ == "__main__":
    A1 = Matrix([[Global_X[1], Global_X[2], Global_X[3]**2, Global_X[1]]])
    A2 = Matrix([[Global_X[4] + Global_X[5], Global_X[5]]])
    A3 = Matrix([[Global_X[6], Global_X[7]]])
    print(A1, A2, A3)
    test = Interface(A1, A2, A3)
    print(test)
    print(GetBusNum(A1, A2, A3))
