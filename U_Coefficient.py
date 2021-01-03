import math
import numpy as np
import sympy
from sympy import Matrix, symbols, Lambda
from Global_X import Global_X

#VA should be given in Votage magnitude & argument in radians forms

num = 2
#num = UI.size()   #from UI (PQ +PV+ VA)
m, n = symbols('m,n')
Global_U_coefficient = sympy.zeros(1, 2* num)


def ef_coefficient(admittance_matrix,  PQ_PV, BusNum):  #e_f_matrix is ei, fi initial value
    size_PQ = BusNum[0]
    size_PV = BusNum[1]
    size_VA = BusNum[2]
    for i in range (size_PQ + size_PV , size_VA + size_PV + size_PQ):
        e_VA = VA[0] * math.cos(math.radians(VA[1]))
        f_VA = VA[0] * math.sin(math.radians(VA[1]))
        Global_U_coefficient[size_PQ+size_PV+2*i-1] = e_VA
        Global_X[size_PQ+size_PV+2*i-1] = e_VA
        Global_U_coefficient[size_PQ+size_PV+2*i] = f_VA
        Global_X[size_PQ+size_PV+2*i] = f_VA
    y_temp_real = np.real(admittance_matrix)
    y_temp_imag = np.imag(admittance_matrix)
    for i in range(0, size_PQ):
        for k in range(0, num):
                Global_U_coefficient[2*i] += (y_temp_real[i][k]*Global_X[2*i] + y_temp_imag[i][k]*Global_X[2*i+1] )\
                                             *Global_X[2*k] + (Global_X[2*i+1]*y_temp_real[i][k] - Global_X[2*i]*
                                              y_temp_imag[i][k]) * Global_X[2*k +1]                                # P_pq coefficient

                Global_U_coefficient[2*i+1] += (-y_temp_real[i][k]*Global_X[2*i] - y_temp_imag[i][k]*Global_X[2*i+1] )\
                                             *Global_X[2*k+1] + (Global_X[2*i+1]*y_temp_real[i][k] - Global_X[2*i]*y_temp_imag[i][k]) \
                                             * Global_X[2*k]              #Q_pq coefficient
        Global_U_coefficient[2*i] -=PQ_PV[i][0]
        Global_U_coefficient[2*i+1] -=PQ_PV[i][1]

    for i in range(size_PQ, size_PQ + size_PV):
        for k in range(0, num):
            Global_U_coefficient[2 * i] += (y_temp_real[i][k]*Global_X[2*i] + y_temp_imag[i][k]*Global_X[2*i+1] )\
                                             *Global_X[2*k] + (Global_X[2*i+1]*y_temp_real[i][k] - Global_X[2*i]*
                                              y_temp_imag[i][k]) * Global_X[2*k +1]    # P_pv coefficient
        Global_U_coefficient[2*i +1] = Global_X[2*i]**2 + Global_X[2*i+1]**2    # V_pv coefficient
        Global_U_coefficient[2*i] -=PQ_PV[i][0]
        Global_U_coefficient[2*i+1] -=(PQ_PV[i][1])**2
    return Global_U_coefficient



'''
if __name__ == "__main__":
    admittance_matrix = np.array([[0.12 -0.16j, -0.12 + 0.16j],
                         [-0.12 + 0.16j, 0.12 - 0.16j]])
    VA = [242000, 0]
    PQ_PV = np.array([[10,20],
             [242, 0]])
    busnum = [1,0,1]
    U_coefficient = ef_coefficient(admittance_matrix, PQ_PV, BusNum = busnum)
    print(U_coefficient)
'''









        #PQ_bus

