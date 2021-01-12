import math
import numpy
from UI_Interface import link_vex, link_edge
# from UI import GraphicScene


def r_1(diameter, line_distance=0):
    r = diameter / 2
    return r


def r_4(diameter, line_distance):
    r = ((diameter / 2) * (line_distance ** 3) * (2 ** 0.5)) ** (1 / 4)
    return r


def r_6(diameter, line_distance):
    r = ((diameter / 2) * (line_distance ** 5) * 6) ** (1 / 6)
    return r


def get_wire(type, Da, Db, Dc, diameter, line_distance, length, S_wire):
    Dm = (Da * Db * Dc) ** (1 / 3)
    if type == 1:  # type 1:cu + n=1
        rou = 18.8
        n = 1
        r = r_1(diameter, line_distance)
        r0 = rou / S_wire  # R / meter
        x0 = 0.1445 * math.log(Dm / r, 10) + 0.0157 / n
        b0 = 7.58 / math.log(Dm / r, 10) * 10 ** (-6)
        g0 = 0
        if length < 300:
            r1 = r0 * length
            x1 = x0 * length
            b1 = b0 * (length / 2)
            g1 = g0 * length
        else:
            kr = 1 - x0 * b0 * (length ** 2) / 3
            kx = 1 - (x0 * b0 - (r0 ** 2) * b0 / x0) * (length ** 2) / 6
            kb = 1 + x0 * b0 * (length ** 2) / 12
            r1 = kr * r0 * length
            x1 = kx * x0 * length
            b1 = kb * b0 * (length / 2)
            g1 = g0 * length
        z = complex(r1, x1)
        yij = 1 / z
        yi0 = complex(g1, b1)
        yj0 = complex(g1, b1)
        return [yij, yi0, yj0]

    if type == 2:  # type 2:cu + n=4 square
        rou = 18.8
        n = 4
        r = r_4(diameter, line_distance)
        r0 = rou / S_wire  # R / meter
        x0 = 0.1445 * math.log(Dm / r, 10) + 0.0157 / n
        b0 = 7.58 / math.log(Dm / r, 10) * 10 ** (-6)
        g0 = 0
        if length < 300:
            r1 = r0 * length
            x1 = x0 * length
            b1 = b0 * (length / 2)
            g1 = g0 * length
        else:
            kr = 1 - x0 * b0 * (length ** 2) / 3
            kx = 1 - (x0 * b0 - (r0 ** 2) * b0 / x0) * (length ** 2) / 6
            kb = 1 + x0 * b0 * (length ** 2) / 12
            r1 = kr * r0 * length
            x1 = kx * x0 * length
            b1 = kb * b0 * (length / 2)
            g1 = g0 * length
        z = complex(r1, x1)
        yij = 1 / z
        yi0 = complex(g1, b1)
        yj0 = complex(g1, b1)
        return [yij, yi0, yj0]

    if type == 3:  # type 3:cu + n=6 hexa
        rou = 18.8
        n = 6
        r = r_6(diameter, line_distance)
        r0 = rou / S_wire  # R / meter
        x0 = 0.1445 * math.log(Dm / r, 10) + 0.0157 / n
        b0 = 7.58 / math.log(Dm / r, 10) * 10 ** (-6)
        g0 = 0
        if length < 300:
            r1 = r0 * length
            x1 = x0 * length
            b1 = b0 * (length / 2)
            g1 = g0 * length
        else:
            kr = 1 - x0 * b0 * (length ** 2) / 3
            kx = 1 - (x0 * b0 - (r0 ** 2) * b0 / x0) * (length ** 2) / 6
            kb = 1 + x0 * b0 * (length ** 2) / 12
            r1 = kr * r0 * length
            x1 = kx * x0 * length
            b1 = kb * b0 * (length / 2)
            g1 = g0 * length
        z = complex(r1, x1)
        yij = 1 / z
        yi0 = complex(g1, b1)
        yj0 = complex(g1, b1)
        return [yij, yi0, yj0]

    if type == 4:  # type 4:AL + n=1
        rou = 31.5
        n = 1
        r = r_1(diameter, line_distance)
        r0 = rou / S_wire  # R / meter
        x0 = 0.1445 * math.log(Dm / r, 10) + 0.0157 / n
        b0 = 7.58 / math.log(Dm / r, 10) * 10 ** (-6)
        g0 = 0
        if length < 300:
            r1 = r0 * length
            x1 = x0 * length
            b1 = b0 * (length / 2)
            g1 = g0 * length
        else:
            kr = 1 - x0 * b0 * (length ** 2) / 3
            kx = 1 - (x0 * b0 - (r0 ** 2) * b0 / x0) * (length ** 2) / 6
            kb = 1 + x0 * b0 * (length ** 2) / 12
            r1 = kr * r0 * length
            x1 = kx * x0 * length
            b1 = kb * b0 * (length / 2)
            g1 = g0 * length
        z = complex(r1, x1)
        yij = 1 / z
        yi0 = complex(g1, b1)
        yj0 = complex(g1, b1)
        return [yij, yi0, yj0]

    if type == 5:  # type 5:AL + n=4 square
        rou = 31.5
        n = 4
        r = r_4(diameter, line_distance)
        r0 = rou / (n * S_wire)  # R / meter
        x0 = 0.1445 * math.log(Dm / r, 10) + 0.0157 / n
        b0 = 7.58 / math.log(Dm / r, 10) * 10 ** (-6)
        g0 = 0
        if length < 300:
            r1 = r0 * length
            x1 = x0 * length
            b1 = b0 * (length / 2)
            g1 = g0 * length
        else:
            kr = 1 - x0 * b0 * (length ** 2) / 3
            kx = 1 - (x0 * b0 - (r0 ** 2) * b0 / x0) * (length ** 2) / 6
            kb = 1 + x0 * b0 * (length ** 2) / 12
            r1 = kr * r0 * length
            x1 = kx * x0 * length
            b1 = kb * b0 * (length / 2)
            g1 = g0 * length
        z = complex(r1, x1)
        yij = 1 / z
        yi0 = complex(g1, b1)
        yj0 = complex(g1, b1)
        return [yij, yi0, yj0]

    if type == 6:  # type 6:AL + n=6 hexa
        rou = 31.5
        n = 6
        r = r_6(diameter, line_distance)
        r0 = rou / S_wire  # R / meter
        x0 = 0.1445 * math.log(Dm / r, 10) + 0.0157 / n
        b0 = 7.58 / math.log(Dm / r, 10) * 10 ** (-6)
        g0 = 0
        if length < 300:
            r1 = r0 * length
            x1 = x0 * length
            b1 = b0 * (length / 2)
            g1 = g0 * length
        else:
            kr = 1 - x0 * b0 * (length ** 2) / 3
            kx = 1 - (x0 * b0 - (r0 ** 2) * b0 / x0) * (length ** 2) / 6
            kb = 1 + x0 * b0 * (length ** 2) / 12
            r1 = kr * r0 * length
            x1 = kx * x0 * length
            b1 = kb * b0 * (length / 2)
            g1 = g0 * length
        z = complex(r1, x1)
        yij = 1 / z
        yi0 = complex(g1, b1)
        yj0 = complex(g1, b1)
        return [yij, yi0, yj0]


def Admittance_wire(nodes, scene):  # type, Da, Db, Dc, diameter, line_distance, length, S_wire
    node_num = len(nodes)
    Topology = numpy.zeros((node_num, node_num), dtype=numpy.complex_)
    for i in range(0, node_num):
        for j in range(0, node_num):
            if link_vex(nodes[i], nodes[j], scene):
                temp_edge = link_edge(nodes[i], nodes[j], scene)
                Topology[i][j] = get_wire(temp_edge.data_dialog.wire_text[0], temp_edge.data_dialog.wire_text[1],
                                          temp_edge.data_dialog.wire_text[2], temp_edge.data_dialog.wire_text[3],
                                          temp_edge.data_dialog.wire_text[4], temp_edge.data_dialog.wire_text[5],
                                          temp_edge.data_dialog.wire_text[6], temp_edge.data_dialog.wire_text[7]
                                          )[
                    0]
                Topology[i][i] = get_wire(temp_edge.data_dialog.wire_text[0], temp_edge.data_dialog.wire_text[1],
                                          temp_edge.data_dialog.wire_text[2], temp_edge.data_dialog.wire_text[3],
                                          temp_edge.data_dialog.wire_text[4], temp_edge.data_dialog.wire_text[5],
                                          temp_edge.data_dialog.wire_text[6], temp_edge.data_dialog.wire_text[7])[
                    1]
                Topology[j][j] = get_wire(temp_edge.data_dialog.wire_text[0], temp_edge.data_dialog.wire_text[1],
                                          temp_edge.data_dialog.wire_text[2], temp_edge.data_dialog.wire_text[3],
                                          temp_edge.data_dialog.wire_text[4], temp_edge.data_dialog.wire_text[5],
                                          temp_edge.data_dialog.wire_text[6], temp_edge.data_dialog.wire_text[7])[
                    2]
    return Topology


# temp_Topology = Admittance_wire(demo.scene.nodes)

'''
if __name__ == '__main__':
    Topology = Admittance_bus(size_n = 2, type=5, Dm=16380, diameter = 24.26, line_distance = 450, length=600, S_wire=300)
    print(Topology)

'''
