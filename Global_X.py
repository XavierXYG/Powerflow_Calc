import sympy
from sympy import Matrix, symbols, Lambda

m, n = symbols('m,n')
num = 3*2     # 不定维矩阵   size_PQ + size_PV + size_VA
Global_X = Matrix(1, num, Lambda((m, n), m + n))
for i in range(num):
    Global_X[i] = sympy.Symbol('x'+str(i))


