# coding=utf8
import numpy as np
import math



def get_admittance_matrix(Topology):
    num_rows = Topology.shape[0]
    num_columns = Topology.shape[1]
    admittance_matrix = np.zeros((num_rows, num_columns), dtype=complex)
    for i in range(num_rows):
        for j in range(num_columns):
            if i == j:
                aux_cal_matrix = np.sum(Topology, axis=1)
                for num in range(num_rows):
                    admittance_matrix[i][j] = aux_cal_matrix[i]
            else:
                admittance_matrix[i][j] = -Topology[i][j]
    return admittance_matrix


if __name__ == "__main__":
<<<<<<< HEAD

    a = 1+j
    b = 1
    print(a+b)

=======
    test = np.array([[1 + 2j, 2 + 3j, 1 + 1j],
                     [3 + 0j, 4 + 5j, 5],
                     [1 + 0j, 2 + 0j, 3 + 0j]])
    result = get_admittance_matrix(test)
    print(result)
'''
>>>>>>> 9ba8ed0f98ee18f47ab3a6f4dcac30ccf8ade91c
