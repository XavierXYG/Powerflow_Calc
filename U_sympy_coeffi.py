import math
import numpy as np
import sympy
from sympy import symbols, Eq, solve
from Global_X import getGlobal_X


# UI will give BusNum and PQ_PV
# BusNum contains numbers of PQ and PV and VA
# PQ_PV contains the P and Q value of PQ, P and V value of PV, V and theta value of VA(generator)
# VA should be given in Votage magnitude & argument in radians forms


def PQ_ef_coefficient(admittance_matrix, PQ_PV, BusNum):  # get the coefficient of PQ_bus
    num = sum(BusNum) * 2
    Global_input = getGlobal_X(num).copy()
    size_PQ = BusNum[0]
    size_PV = BusNum[1]
    size_VA = BusNum[2]
    PQ_bus = sympy.zeros(1, 2 * size_PQ)
    y_temp_real = np.real(admittance_matrix)
    y_temp_imag = np.imag(admittance_matrix)
    for i in range(0,
                   size_VA):  # change the x of VA in Global_input into VA value(since they are not variable, they are constant)
        e_VA = PQ_PV[size_PQ + size_PV + i][0] * math.cos(math.radians(PQ_PV[size_PQ + size_PV + i][1]))
        f_VA = PQ_PV[size_PQ + size_PV + i][0] * math.sin(math.radians(PQ_PV[size_PQ + size_PV + i][1]))
        Global_input[2 * (size_PQ + size_PV) + 2 * i] = e_VA
        Global_input[(size_PQ + size_PV) * 2 + 2 * i + 1] = f_VA

    for i in range(0, size_PQ):
        for k in range(0, int(num / 2)):
            PQ_bus[2 * i] += (y_temp_real[i][k] * Global_input[2 * i] + y_temp_imag[i][k] * Global_input[2 * i + 1]) \
                             * Global_input[2 * k] + (
                                     Global_input[2 * i + 1] * y_temp_real[i][k] - Global_input[2 * i] *
                                     y_temp_imag[i][k]) * Global_input[2 * k + 1]  # P_pq coefficient

            PQ_bus[2 * i + 1] += (-y_temp_real[i][k] * Global_input[2 * i] - y_temp_imag[i][k] * Global_input[
                2 * i + 1]) \
                                 * Global_input[2 * k + 1] + (
                                         Global_input[2 * i + 1] * y_temp_real[i][k] - Global_input[2 * i] *
                                         y_temp_imag[i][k]) \
                                 * Global_input[2 * k]  # Q_pq coefficient
        PQ_bus[2 * i] += PQ_PV[i][0]  # P_pq coefficient - P(value from UI )
        PQ_bus[2 * i + 1] += PQ_PV[i][1]  # Q_pq coefficient - Q(value from UI )

        PQ_bus[2 * i] = Eq(PQ_bus[2 * i])  # P_pq coefficient - P(value from UI )
        PQ_bus[2 * i + 1] = Eq(PQ_bus[2 * i + 1])  # Q_pq coefficient - Q(value from UI )
    return PQ_bus  # P1, Q1, P2, Q2... coefficient


def PV_ef_coefficient(admittance_matrix, PQ_PV, BusNum):  # get the coefficient of PV_bus
    num = sum(BusNum) * 2
    Global_input = getGlobal_X(num).copy()
    size_PQ = BusNum[0]
    size_PV = BusNum[1]
    size_VA = BusNum[2]
    PV_bus = sympy.zeros(1, 2 * size_PV)
    y_temp_real = np.real(admittance_matrix)
    y_temp_imag = np.imag(admittance_matrix)
    for i in range(0, size_VA):
        e_VA = PQ_PV[size_PQ + size_PV + i][0] * math.cos(math.radians(PQ_PV[size_PQ + size_PV + i][1]))
        f_VA = PQ_PV[size_PQ + size_PV + i][0] * math.sin(math.radians(PQ_PV[size_PQ + size_PV + i][1]))
        Global_input[2 * (size_PQ + size_PV) + 2 * i] = e_VA
        Global_input[(size_PQ + size_PV) * 2 + 2 * i + 1] = f_VA

    for i in range(0, size_PV):
        for k in range(0, int(num / 2)):
            PV_bus[2 * i] += (y_temp_real[i + size_PQ][k] * Global_input[2 * (i + size_PQ)] + y_temp_imag[i + size_PQ][
                k] * Global_input[2 * (i + size_PQ) + 1]) \
                             * Global_input[2 * k] + (
                                     Global_input[2 * (i + size_PQ) + 1] * y_temp_real[i + size_PQ][k] -
                                     Global_input[2 * (i + size_PQ)] *
                                     y_temp_imag[i + size_PQ][k]) * Global_input[2 * k + 1]  # P_pv coefficient
        PV_bus[2 * i + 1] = Global_input[2 * (i + size_PQ)] ** 2 + Global_input[
            2 * (i + size_PQ) + 1] ** 2  # V_pv coefficient
        PV_bus[2 * i] += PQ_PV[size_PQ + i][0]  # P_pv coefficient - P(value from UI )
        PV_bus[2 * i + 1] -= (PQ_PV[size_PQ + i][1]) ** 2  # V_pv coefficient - V**2(value from UI )

        PV_bus[2 * i] = Eq(PV_bus[2 * i])  # P_pq coefficient - P(value from UI )
        PV_bus[2 * i + 1] = Eq(PV_bus[2 * i + 1])  # Q_pq coefficient - Q(value from UI )
    if any(PV_bus) == 0:
        return PV_bus  # P1, V1, P2, V2... coefficient
    else:
        return PV_bus[0]


def VA_ef_coefficient(PQ_PV, BusNum):  # get the coefficient of VA_bus
    num = sum(BusNum) * 2
    size_PQ = BusNum[0]
    size_PV = BusNum[1]
    size_VA = BusNum[2]
    VA_bus = sympy.zeros(1, 2 * size_VA)
    for i in range(0, size_VA):
        e_VA = PQ_PV[size_PQ + size_PV + i][0] * math.cos(math.radians(PQ_PV[size_PQ + size_PV + i][1]))
        f_VA = PQ_PV[size_PQ + size_PV + i][0] * math.sin(math.radians(PQ_PV[size_PQ + size_PV + i][1]))
        # Global_X[num - size_VA*2 ] = e_VA
        # Global_X[num - size_VA*2+1] = f_VA
        VA_bus[2 * i] = getGlobal_X(num)[num - size_VA * 2] - e_VA
        VA_bus[2 * i + 1] = getGlobal_X(num)[num - size_VA * 2 + 1] - f_VA

        VA_bus[2 * i] = Eq(VA_bus[2 * i])  # P_pq coefficient - P(value from UI )
        VA_bus[2 * i + 1] = Eq(VA_bus[2 * i + 1])  # Q_pq coefficient - Q(value from UI )
    return VA_bus  # e_VA1, f_VA1, e_VA2, e_VA2... coefficient


def sum_coefficient(PQ_bus, PV_bus, VA_bus, BusNum):
    # temp = sympy.zeros(sum(BusNum)*2)
    temp = getGlobal_X(sum(BusNum)*2).copy()
    size_PQ = BusNum[0]
    size_PV = BusNum[1]
    size_VA = BusNum[2]
    for item1 in range(0, size_PQ*2):
        temp[item1] = PQ_bus[item1]
    for item2 in range(size_PQ*2, 2*(size_PQ+size_PV)):
        temp[item2] = PV_bus[item2]
    for item3 in range(2*(size_PQ+size_PV), 2*(size_PQ+size_PV+size_VA)):
        temp[item3] = VA_bus[item3-2*(size_PQ+size_PV)]
    return temp


if __name__ == "__main__":
    admittance_matrix = np.array([[0.12 - 0.16j, -0.12 + 0.16j],
                                  [-0.12 + 0.16j, 0.12 - 0.16j]])
    PQ_PV = np.array([[10000000, 20000000],
                      [242000, 0]])
    busnum = [1, 0, 1]
    PQ_coefficient = PQ_ef_coefficient(admittance_matrix, PQ_PV, BusNum=busnum)
    PV_coefficient = PV_ef_coefficient(admittance_matrix, PQ_PV, BusNum=busnum)
    VA_coefficient = VA_ef_coefficient(PQ_PV, BusNum=busnum)

    print(PQ_coefficient, PV_coefficient, VA_coefficient)
    print(sum_coefficient(PQ_coefficient,PV_coefficient,VA_coefficient,busnum))
