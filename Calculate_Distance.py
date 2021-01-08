# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 21:47:36 2021

@author: dell
"""
import numpy as np
import math


# 计算点到直线的距离
def get_distance_from_point_to_line(point, line_point1, line_point2):
    # 对于两点坐标为同一点时,返回点与点的距离
    if line_point1 == line_point2:
        point_array = np.array(point)
        point1_array = np.array(line_point1)
        return np.linalg.norm(point_array - point1_array)
    # 计算直线的三个参数
    A = line_point2[1] - line_point1[1]
    B = line_point1[0] - line_point2[0]
    C = (line_point1[1] - line_point2[1]) * line_point1[0] + \
        (line_point2[0] - line_point1[0]) * line_point1[1]
    # 根据点到直线的距离公式计算距离
    distance = np.abs(A * point[0] + B * point[1] + C) / (np.sqrt(A ** 2 + B ** 2))
    return distance


# 计算点到线段的距离
def PointToSegDist(x, y, x1, y1, x2, y2):
    cross = (x2 - x1) * (x - x1) + (y2 - y1) * (y - y1)
    # |AB*AP|：矢量乘
    if cross <= 0:
        return math.sqrt((x - x1) * (x - x1) + (y - y1) * (y - y1))
        # 是|AP|：矢量的大小
    d2 = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)
    # |AB|^2：矢量AB的大小的平方
    if cross >= d2:
        return math.sqrt((x - x2) * (x - x2) + (y - y2) * (y - y2))
    # 是|BP|：矢量的大小

    r = cross / d2  # //相似三角形原理求出c点的坐标
    px = x1 + (x2 - x1) * r
    py = y1 + (y2 - y1) * r
    return math.sqrt((x - px) * (x - px) + (py - y) * (py - y))


def calculate_distance(src_coordinate, dst_coordinate, list_pos):
    x1 = src_coordinate[0]
    y1 = src_coordinate[1]
    x2 = dst_coordinate[0]
    y2 = dst_coordinate[1]
    x = list_pos[0]
    y = list_pos[1]
    alpha = 0.1
    x_1 = x1 + alpha * (x2-x1)
    x_2 = x2 - alpha * (x2 - x1)
    y_1 = y1 + alpha * (y2 - y1)
    y_2 = y2 - alpha * (y2 - y1)
    # distance=get_distance_from_point_to_line(point, line_point1, line_point2)
    distance = PointToSegDist(x, y, x_1, y_1, x_2, y_2)
    return distance


# if __name__ == '__main__':
#     print(calculate_distance([1, 2],[2, 3], [4, 5]))
