import math
import numpy as np
import sympy
from sympy import Matrix, symbols, Lambda
from Global_X import Global_X

#VA should be given in Votage magnitude & argument in radians forms

num = 2
#num = UI.size()   #from UI (PQ +PV+ VA)



def PQ_ef_coefficient(admittance_matrix,  PQ_PV, BusNum):  #e_f_matrix is ei, fi initial value
    size_PQ = BusNum[0]
    size_PV = BusNum[1]
    size_VA = BusNum[2]
    PQ_bus = sympy.zeros(1, 2 * size_PQ)
    y_temp_real = np.real(admittance_matrix)
    y_temp_imag = np.imag(admittance_matrix)
    for i in range (0, size_VA ):
        e_VA = PQ_PV[size_PQ + size_PV + i][0] * math.cos(math.radians(PQ_PV[size_PQ + size_PV + i][1]))
        f_VA = PQ_PV[size_PQ + size_PV + i][0] * math.sin(math.radians(PQ_PV[size_PQ + size_PV + i][1]))
        Global_X[size_PQ+size_PV+2*i+1] = e_VA
        Global_X[size_PQ+size_PV+2*i+2] = f_VA

    for i in range(0, size_PQ):
        for k in range(0, num):
                PQ_bus[2*i] += (y_temp_real[i][k]*Global_X[2*i] + y_temp_imag[i][k]*Global_X[2*i+1] )\
                                             *Global_X[2*k] + (Global_X[2*i+1]*y_temp_real[i][k] - Global_X[2*i]*
                                              y_temp_imag[i][k]) * Global_X[2*k +1]                                # P_pq coefficient

                PQ_bus[2*i+1] += (-y_temp_real[i][k]*Global_X[2*i] - y_temp_imag[i][k]*Global_X[2*i+1] )\
                                             *Global_X[2*k+1] + (Global_X[2*i+1]*y_temp_real[i][k] - Global_X[2*i]*y_temp_imag[i][k]) \
                                             * Global_X[2*k]              #Q_pq coefficient
        PQ_bus[2*i] -=PQ_PV[i][0]
        PQ_bus[2*i+1] -=PQ_PV[i][1]
    return PQ_bus


def PV_ef_coefficient(admittance_matrix,  PQ_PV, BusNum):
    size_PQ = BusNum[0]
    size_PV = BusNum[1]
    size_VA = BusNum[2]
    PV_bus = sympy.zeros(1, 2 * size_PV)
    y_temp_real = np.real(admittance_matrix)
    y_temp_imag = np.imag(admittance_matrix)
    for i in range (0, size_VA ):
        e_VA = PQ_PV[size_PQ + size_PV + i][0] * math.cos(math.radians(PQ_PV[size_PQ + size_PV + i][1]))
        f_VA = PQ_PV[size_PQ + size_PV + i][0] * math.sin(math.radians(PQ_PV[size_PQ + size_PV + i][1]))
        Global_X[size_PQ+size_PV+2*i+1] = e_VA
        Global_X[size_PQ+size_PV+2*i+2] = f_VA

    for i in range(0, size_PV):
        for k in range(0, num):
            PV_bus[2 * i] += (y_temp_real[i+size_PQ][k]*Global_X[2*(i+size_PQ)] + y_temp_imag[i+size_PQ][k]*Global_X[2*(i+size_PQ)+1] )\
                                             *Global_X[2*k] + (Global_X[2*(i+size_PQ)+1]*y_temp_real[i+size_PQ][k] - Global_X[2*(i+size_PQ)]*
                                              y_temp_imag[i+size_PQ][k]) * Global_X[2*k +1]    # P_pv coefficient
        PV_bus[2*i +1] = Global_X[2*(i+size_PQ)]**2 + Global_X[2*(i+size_PQ)+1]**2    # V_pv coefficient
        PV_bus[2*i] -=PQ_PV[size_PQ+i][0]
        PV_bus[2*i+1] -=(PQ_PV[size_PQ+i][1])**2
    return PV_bus



def VA_ef_coefficient(admittance_matrix,  PQ_PV, BusNum):
    size_PQ = BusNum[0]
    size_PV = BusNum[1]
    size_VA = BusNum[2]
    VA_bus = sympy.zeros(1, 2 * size_VA)
    for i in range (0, size_VA ):
        e_VA = PQ_PV[size_PQ+size_PV+i][0] * math.cos(math.radians(PQ_PV[size_PQ+size_PV+i][1]))
        f_VA = PQ_PV[size_PQ+size_PV+i][0] * math.sin(math.radians(PQ_PV[size_PQ+size_PV+i][1]))
        VA_bus[2*i] = e_VA
        VA_bus[2*i+1] = f_VA
    return VA_bus

'''
if __name__ == "__main__":
    admittance_matrix = np.array([[0.12 -0.16j, -0.12 + 0.16j],
                         [-0.12 + 0.16j, 0.12 - 0.16j]])
    PQ_PV = np.array([[10,20],
             [242000, 0]])
    busnum = [1,0,1]
    PQ_coefficient = PQ_ef_coefficient(admittance_matrix, PQ_PV, BusNum = busnum)
    PV_coefficient = PV_ef_coefficient(admittance_matrix, PQ_PV, BusNum = busnum)
    VA_coefficient = VA_ef_coefficient(admittance_matrix, PQ_PV, BusNum = busnum)
    print(PQ_coefficient, PV_coefficient, VA_coefficient)
'''











