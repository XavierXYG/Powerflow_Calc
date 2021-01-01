import math
import numpy


def r_1(diameter, line_distance = 0):
    r = diameter/2
    return r


def r_4(diameter, line_distance):
    r = ((diameter/2)*(line_distance**3)*(2**0.5))**(1/6)
    return r


def r_6(diameter, line_distance):
    r = ((diameter/2)*(line_distance**5)*6)**(1/6)
    return r


def get_wire(type, Dm, diameter, line_distance, length, S_wire):
    if type == 1:       #type 1:cu + n=1
        rou = 18.8
        n = 1
        r = r_1(diameter, line_distance)
        r0 = rou/S_wire       #R / meter
        x0 = 0.1445*math.log(Dm/r, 10) + 0.0157/n
        b0 = 7.58 / math.log(Dm/r, 10) * 10**(-6)
        g0 = 0
        if length< 300:
            r1 = r0 * length
            x1 = x0 * length
            b1 = b0 * (length/2)
            g1 = g0 * length
        else:
            kr = 1 - x0*b0*(length^2)/3
            kx = 1 - (x0 * b0 - (r0^2)*b0/x0)*(length^2)/6
            kb = 1 + x0*b0*(length^2)/12
            r1 = kr * r0 * length
            x1 = kx * x0 * length
            b1 = kb * b0 * (length/2)
            g1 = g0 * length
        z = r1 +x1j
        yij = 1/z
        yi0 = b1 + g1j
        return [yij, yi0]

    if type == 2:       #type 2:cu + n=4 square
        rou = 18.8
        n = 4
        r = r_4(diameter, line_distance)
        r0 = rou/S_wire       #R / meter
        x0 = 0.1445*math.log(Dm/r, 10) + 0.0157/n
        b0 = 7.58 / math.log(Dm/r, 10) * 10**(-6)
        g0 = 0
        if length< 300:
            r1 = r0 * length
            x1 = x0 * length
            b1 = b0 * (length/2)
            g1 = g0 * length
        else:
            kr = 1 - x0*b0*(length^2)/3
            kx = 1 - (x0 * b0 - (r0^2)*b0/x0)*(length^2)/6
            kb = 1 + x0*b0*(length^2)/12
            r1 = kr * r0 * length
            x1 = kx * x0 * length
            b1 = kb * b0 * (length/2)
            g1 = g0 * length
        z = r1 +x1j
        yij = 1/z
        yi0 = b1 + g1j
        return [yij, yi0]


    if type == 3:       #type 3:cu + n=6 hexa
        rou = 18.8
        n = 6
        r = r_6(diameter, line_distance)
        r0 = rou/S_wire       #R / meter
        x0 = 0.1445*math.log(Dm/r, 10) + 0.0157/n
        b0 = 7.58 / math.log(Dm/r, 10) * 10**(-6)
        g0 = 0
        if length< 300:
            r1 = r0 * length
            x1 = x0 * length
            b1 = b0 * (length/2)
            g1 = g0 * length
        else:
            kr = 1 - x0*b0*(length^2)/3
            kx = 1 - (x0 * b0 - (r0^2)*b0/x0)*(length^2)/6
            kb = 1 + x0*b0*(length^2)/12
            r1 = kr * r0 * length
            x1 = kx * x0 * length
            b1 = kb * b0 * (length/2)
            g1 = g0 * length
        z = r1 +x1j
        yij = 1/z
        yi0 = b1 + g1j
        return [yij, yi0]



    if type == 4:       #type 4:AL + n=1
        rou = 31.5
        n = 1
        r = r_1(diameter, line_distance)
        r0 = rou/S_wire       #R / meter
        x0 = 0.1445*math.log(Dm/r, 10) + 0.0157/n
        b0 = 7.58 / math.log(Dm/r, 10) * 10**(-6)
        g0 = 0
        if length< 300:
            r1 = r0 * length
            x1 = x0 * length
            b1 = b0 * (length/2)
            g1 = g0 * length
        else:
            kr = 1 - x0*b0*(length^2)/3
            kx = 1 - (x0 * b0 - (r0^2)*b0/x0)*(length^2)/6
            kb = 1 + x0*b0*(length^2)/12
            r1 = kr * r0 * length
            x1 = kx * x0 * length
            b1 = kb * b0 * (length/2)
            g1 = g0 * length
        z = r1 +x1j
        yij = 1/z
        yi0 = b1 + g1j
        return [yij, yi0]



    if type == 5:       #type 5:AL + n=4 square
        rou = 31.5
        n = 4
        r = r_4(diameter, line_distance)
        r0 = rou/S_wire       #R / meter
        x0 = 0.1445*math.log(Dm/r, 10) + 0.0157/n
        b0 = 7.58 / math.log(Dm/r, 10) * 10**(-6)
        g0 = 0
        if length< 300:
            r1 = r0 * length
            x1 = x0 * length
            b1 = b0 * (length/2)
            g1 = g0 * length
        else:
            kr = 1 - x0*b0*(length^2)/3
            kx = 1 - (x0 * b0 - (r0^2)*b0/x0)*(length^2)/6
            kb = 1 + x0*b0*(length^2)/12
            r1 = kr * r0 * length
            x1 = kx * x0 * length
            b1 = kb * b0 * (length/2)
            g1 = g0 * length
        z = r1 +x1j
        yij = 1/z
        yi0 = b1 + g1j
        return [yij, yi0]


    if type == 6:       #type 6:AL + n=6 hexa
        rou = 31.5
        n = 6
        r = r_6(diameter, line_distance)
        r0 = rou/S_wire       #R / meter
        x0 = 0.1445*math.log(Dm/r, 10) + 0.0157/n
        b0 = 7.58 / math.log(Dm/r, 10) * 10**(-6)
        g0 = 0
        if length< 300:
            r1 = r0 * length
            x1 = x0 * length
            b1 = b0 * (length/2)
            g1 = g0 * length
        else:
            kr = 1 - x0*b0*(length^2)/3
            kx = 1 - (x0 * b0 - (r0^2)*b0/x0)*(length^2)/6
            kb = 1 + x0*b0*(length^2)/12
            r1 = kr * r0 * length
            x1 = kx * x0 * length
            b1 = kb * b0 * (length/2)
            g1 = g0 * length
        z = r1 +x1j
        yij = 1/z
        yi0 = b1 + g1j
        return [yij, yi0]


def Admittance_bus():
    Topology = np.zeros(size_n)   #size_n is number of bus
    for i in range(1, size_n):
        for j in range(1, size_n):
            if(link_vex()):    # link_vex()  judge the connection of bus
                Topology[i][j] = get_wire(type, Dm, diameter, line_distance, length, S_wire)[0]
                Topology[i][i] = get_wire(type, Dm, diameter, line_distance, length, S_wire)[1]
            return Topology




