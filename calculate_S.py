import math
import numpy


def power_flow(U_matrix, admittance_matrix):
    size_n = int(numpy.array(U_matrix).shape[0] /2)
    S_Topology = numpy.zeros((size_n, size_n), dtype=numpy.complex_)
    delta_S_Topology = numpy.zeros((size_n, size_n), dtype=numpy.complex_)
    y_gnd = numpy.sum(admittance_matrix, axis=1)
    for i in range(0, size_n):
        for j in range(0,size_n):
            if (link_vex()):
                ui = complex(U_matrix[i], U_matrix[i + size_n])
                uj = complex(U_matrix[j], U_matrix[j + size_n])
                yi0 = y_gnd[i]
                yj0 = y_gnd[j]
                yij = (0 + 0j) - admittance_matrix[i][j]
                if i==j:
                    S_Topology[i][i] = 0
                    delta_S_Topology[i][i] = ui*ui.conjugate()*yi0.conjugate()                #delta [i][i] calculate the delta S to ground(yi0)
                else:
                    S_Topology[i][j] = ui*(
                                ui.conjugate()*yi0.conjugate() + (ui.conjugate()-uj.conjugate())*yij.conjugate())
                    S_Topology[j][i] = uj * (
                                uj.conjugate() * yj0.conjugate() + (uj.conjugate() - ui.conjugate()) * yij.conjugate())
                    delta_S_Topology[i][j] = S_Topology[i][j] + S_Topology[j][i]
                    delta_S_Topology[j][i] = delta_S_Topology[i][j]
    return [S_Topology, delta_S_Topology]



'''
if __name__ =='__main__':
    U = [210, 205, 40, 20]
    y_admittance= numpy.zeros((2,2), dtype=numpy.complex_)
    y_admittance[0][0] = complex((1/65), -(3/130)+1e-4)
    y_admittance[0][1] = complex(-(1/65), (3/130))
    y_admittance[1][0] = complex(-(1/65), (3/130))
    y_admittance[1][1] = complex((1/65), -(3/130)+1e-4)

    S_Topology = power_flow(U, y_admittance)
    print(S_Topology)
'''

