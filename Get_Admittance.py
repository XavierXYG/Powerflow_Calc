import numpy as np

def get_admittance_matrix(Topology):
    num_rows = Topology.shape[0]
    num_columns = Topology.shape[1]
    admittance_matrix = np.zeros((num_rows, num_columns))
    for i in range(num_rows):
        for j in range(num_columns):
            if i == j:
                aux_cal_matrix = np.sum(Topology, axis=0)
                for num in range(num_rows):
                    admittance_matrix[i][j] = aux_cal_matrix[i]
            else:
                admittance_matrix[i][j] = -Topology[i][j]
    return admittance_matrix

'''
if __name__ == "__main__":
    test = np.array([[1, 2, 1],
                    [3, 4, 5],
                    [1, 2, 3]])
    result = get_admittance_matrix(test)
    print(result)
'''