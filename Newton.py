# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 21:03:21 2021

@author: dell
"""
import math
from numpy import *
import matplotlib.pyplot as plt
from Interface import  Interface
from Global_X import  num
from sympy import Matrix, lambdify, symbols, Lambda

'''方程组在这里，三个变量分别是x的三个分量，num是未知数个数，F是传入的等式左边的向量，这里面要整理成f(x)=0的形式
所以要减去右端的Y'''

'''
def Fun(x, num):
    i = num
    f = np.zeros((i), dtype=float)
    # f[0] = x[0] * x[1] - x[2] * x[2] - 1.
    # f[1] = x[0] * x[1] * x[2] + x[1] * x[1] - x[0] * x[0] - 2.
    # f[2] = math.exp(x[0]) + x[2] - math.exp(x[1]) - 3.
    # for i in range(i):
    #     f[i] = F[i] - YYY[i]
    print(f[0])
    return f
'''

# 计算雅可比矩阵的逆矩阵
def dfun(x, num):
    df = np.zeros((num, num), dtype=float)
    dx = 0.00001  # 差分精度
    x1 = np.copy(x)
    for i in range(0, num):  # 求导数，i是列，j是行
        for j in range(0, num):
            x1 = np.copy(x)
            x1[j] = x1[j] + dx  # x+dx
            a = (Interface(x1)[i][0] - Interface(x)[i][0]) / dx  # f(x+dx)-f（x）/dx
            df[i, j] = a
    df_1 = np.linalg.inv(df)  # 计算逆矩阵
    return df_1


def Newton(x, num, accuracy):
    x1 = np.copy(x)
    i = 0
    delta = np.copy(x)
    while (np.sum(abs(delta)) > accuracy and i < 100):  # 控制循环次数
        test = Interface(x).squeeze()
        x1 = x - dot(dfun(x, num), test.T)  # 公式
        delta = x1 - x  # 比较x的变化
        x = x1
        i = i + 1
        # print(x)                      #输出每次迭代的结果
    return x


#############################################################

# def calculate_Global_Y(*args):  # 要求输入的顺序为P1，Q1，P2,Q2
#     num = len(args)
#     for i in range(num):
#         Global_Y.append(args[i])

# 整合牛顿迭代,与主函数相联系
def Newton_iteration(global_Y, F, accuracy):
    num = len(global_Y)  # 可以传到后面去
    x = np.zeros((num), dtype=float)  # 先把x所有的分量置零
    accuracy = accuracy
    result = Newton(x, num, accuracy)  # result就是牛顿迭代法计算的解
    print(result)  # 输出最终迭代的结果，即方程的解


#################################################
# 测试
x = np.ones((6), dtype=float)

accuracy = 1e-6
# F表达式矩阵
# m, n = symbols('m,n')
# num = 4*2     # 不定维矩阵   size_PQ + size_PV + size_VA
# x = Matrix(1, num, Lambda((m, n), m + n))

#print(F)
#Newton_iteration(global_Y, F, accuracy)
if __name__ == "__main__":
    a=Newton(x, num, accuracy)
    print(a)
