# Author Xavier Gao
# Jan 1, 2021

import numpy as np
import math
import queue


class Transformer:
    def __init__(self, Sn, Pk, Uk, Po, Io, Uh, Ul, hn, ln):  # Sn(MVA),Pk(kW),Uk(%),Po(kW),Io(%),Uh(kV),Ul(kV)
        self.direction = 0  # case 1: Un = Uh; case 0: Un = Ul
        self.Uh = Uh
        self.Ul = Ul
        if self.direction:
            self.Un = Uh
        else:
            self.Un = Ul
        self.Rt = Pk * self.Un ** 2 / (1000 * Sn ** 2)
        self.Xt = Uk * self.Un ** 2 / (100 * Sn)
        self.Gt = Po / (1000 * self.Un ** 2)
        self.Bt = -Io * Sn / (100 * self.Un ** 2)  # should be minos because of conductance
        self.ratio = Uh / Ul
        self.hn = hn  # higher voltage level neighbour bus
        self.ln = ln  # lower voltage level neighbour bus


class Bus:
    def __init__(self, admittance, voltage_level, is_initialized):
        self.admittance_ = admittance
        self.voltage_level_ = voltage_level
        self.is_marked_ = False
        self.is_initialized_ = is_initialized
        self.previous_level_ = voltage_level

    @classmethod
    def zero(cls):
        return Bus(0, 0, False)


class Network:
    def __init__(self, topology, *args):
        self.tfs_ = args
        self.bus_ = []
        self.adj_ = topology
        self.Un_ = 0
        self.origin_ = -1
        self.adjacent_queue_ = queue.Queue()
        self.num_ = topology.shape[0]
        self.end_loop_ = []  # to store buses in the ring whose all adjacent neighbours have been marked when traversing

    # def set_tfs(self, *args):
    #     for tf_i in args:
    #         self.tfs_.append(tf_i)

    # def rise_error(self):
    #     print("Error! Two transmission line connected together without a transformer inserted.")

    def construct_graph(self):
        for i in range(self.num_):
            self.bus_.append(Bus.zero())

        # manipulate the effect of transformers
        for tf_i in self.tfs_:
            if tf_i.Uh > self.Un_:
                self.Un_ = tf_i.Uh
            hn = tf_i.hn
            ln = tf_i.ln
            R = tf_i.Rt
            X = tf_i.Xt
            G_wire = R / (R ** 2 + X ** 2)
            B_wire = -X / (R ** 2 + X ** 2)

            # implement bus to ground
            self.adj_[ln, ln] += complex(tf_i.Gt, tf_i.Bt)

            # implement bus
            self.bus_[ln].voltage_level_ = tf_i.Ul
            self.bus_[ln].is_initialized_ = True

            self.bus_[hn].voltage_level_ = tf_i.Uh
            self.bus_[hn].is_initialized_ = True

            # implement transmission line
            self.adj_[hn, ln] += complex(G_wire, B_wire)  # just now should be zero, but no matter, we use +=,
            self.adj_[ln, hn] += complex(G_wire, B_wire)  # because a transformer is not a transmission line

        # manipulate the left unknown buses, which are at the rear or head
        for i in range(self.num_):
            if not self.bus_[i].is_initialized_:
                for j in range(self.num_):
                    if self.adj_[i][j] != 0 and self.bus_[j].is_initialized_:
                        # no transformer here, because it would have been initialized if there is one.
                        self.bus_[i].voltage_level_ = self.bus_[j].voltage_level_
                self.bus_[i].is_initialized_ = True

    def regulate_voltage_level(self, bus_index):
        neighbour_cnt = 0
        unmarked_cnt = 0
        for i in range(self.num_):
            if self.adj_[bus_index][i] != 0 and i != bus_index:
                neighbour_cnt += 1
                if not self.bus_[i].is_marked_:
                    unmarked_cnt += 1
                    self.adjacent_queue_.put(i)
                    self.bus_[i].is_marked_ = True
                    if self.bus_[i].voltage_level_ < self.Un_:
                        k = self.Un_ / self.bus_[i].voltage_level_
                        self.adj_[bus_index][i] /= k ** 2
                        self.adj_[i][bus_index] /= k ** 2
                        self.adj_[i][i] /= k ** 2
                        self.bus_[i].previous_level_ = self.bus_[i].voltage_level_
                        self.bus_[i].voltage_level_ *= k

        # buses in the ring whose all adjacent neighbours have been marked when traversing
        if neighbour_cnt and not unmarked_cnt:
            self.end_loop_.append(bus_index)

    def graph_BFS(self):
        # choose bus with level == Un as origin
        for i in range(self.num_):
            if self.bus_[i].voltage_level_ == self.Un_:
                self.origin_ = i
                break

        # enqueue the origin
        self.adjacent_queue_.put(self.origin_)
        self.bus_[self.origin_].is_marked_ = True

        # while queue != empty，dequeue all and manipulate the dequeued ones.
        # Everytime we dequeue one, and enqueue all unmarked neighbours
        while not self.adjacent_queue_.empty():
            self.regulate_voltage_level(self.adjacent_queue_.get())

        # manipulate end loop buses
        # to avoid the admittance level of the transmission line being different from two buses nearby
        for i in self.end_loop_:
            for j in self.end_loop_:
                if i != j:
                    k = self.Un_ / ((self.bus_[i].previous_level_ + self.bus_[j].previous_level_) * 0.5)
                    self.adj_[i, j] /= k ** 2

    def U_init(self):
        return self.Un_

    def transform(self):
        self.construct_graph()
        self.graph_BFS()
        return self.adj_


# Topology = np.zeros((5, 5), dtype=complex)
Topology = np.array([[0, complex(21, 95.4), 0, 0, 21 + 95.4j],
                     [21 + 95.4j, 0, 0, 0, 0],
                     [0, 0, 0, 105.9 + 481.2j, 0],
                     [0, 0, 105.9 + 481.2j, 0, 0],
                     [21 + 95.4j, 0, 0, 0, 0]], dtype=complex)

# local test
if __name__ == '__main__':
    tf1 = Transformer(400, 500, 5, 100, 2, 231, 121, 1, 2)
    tf2 = Transformer(400, 500, 5, 100, 2, 231, 110, 4, 3)

    network_1 = Network(Topology, tf1, tf2)
    Topology = network_1.transform()
    print(Topology)
