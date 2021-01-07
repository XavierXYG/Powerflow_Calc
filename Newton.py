# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 21:03:21 2021

@author: dell
"""

from numpy import *
from Interface import  Interface
from Global_X import  num
from sympy import Matrix, lambdify, symbols, Lambda

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

#################################################
# 测试
x = np.ones((6), dtype=float)
accuracy = 1e-6
#num在interface里给出
if __name__ == "__main__":
    a=Newton(x, num, accuracy)
    print(a)
