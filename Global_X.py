import sympy
from sympy import Matrix, symbols, Lambda
import UI


def getGlobal_X(num):
    m, n = symbols('m,n')
    temp_num = num  # 不定维矩阵   size_PQ + size_PV + size_VA
    Global_X = Matrix(1, temp_num, Lambda((m, n), m + n))
    for i in range(temp_num):
        Global_X[i] = sympy.Symbol('x' + str(i))
    return Global_X
