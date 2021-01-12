from UI import *
from Edge import Edge


def link_vex(node1, node2, scene):
    for gr_edge in scene.edges:
        start_node = gr_edge.edge_wrap.start_item
        end_node = gr_edge.edge_wrap.end_item
        if node1 == start_node:
            if node2 == end_node:
                return True
        elif node2 == start_node:
            if node1 == end_node:
                return True
    return False


