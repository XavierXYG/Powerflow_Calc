# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 21:03:21 2021

@author: dell
"""

import numpy as np
from numpy import *
from Interface import Interface
from sympy import Matrix, lambdify, symbols, Lambda



# 计算雅可比矩阵的逆矩阵
def dfun(x, num, Global_Y, BusNum, admittance_matrix):
    df = np.zeros((num, num), dtype=float)
    dx = 0.00001  # 差分精度
    x1 = np.copy(x)
    for i in range(0, num):  # 求导数，i是列，j是行
        for j in range(0, num):
            x1 = np.copy(x)
            x1[j] = x1[j] + dx  # x+dx
            a = (Interface(x1, Global_Y, BusNum, admittance_matrix)[i][0] - Interface(x, Global_Y, BusNum, admittance_matrix)[i][0]) / dx  # f(x+dx)-f（x）/dx
            df[i, j] = a
    df_1 = np.linalg.inv(df)  # 计算逆矩阵
    return df_1


def Newton(x, num, accuracy, Global_Y, BusNum, admittance_matrix):
    x1 = np.copy(x)
    i = 0
    delta = np.copy(x)
    while np.sum(abs(delta)) > accuracy and i < 500:  # 控制循环次数
        squeezed_x = Interface(x, Global_Y, BusNum, admittance_matrix).squeeze()
        x1 = x - dot(dfun(x, num, Global_Y, BusNum, admittance_matrix), squeezed_x.T)  # 公式
        delta = x1 - x  # 比较x的变化
        x = x1
        i = i + 1
        # print(x)                      #输出每次迭代的结果
    return x


#################################################
'''
# 测试
x = np.ones(4, dtype=float)*200000
accuracy = 1e-6
# num在interface里给出

#if __name__ == "__main__":
    #a = Newton(x, num, accuracy)
    #print(a)
'''