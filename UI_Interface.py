def link_vex(node1, node2, scene):
    for edge in scene.edges:
        start_node = edge.start_item
        end_node = edge.end_item
        if node1 == start_node:
            if node2 == end_node:
                return True
        elif node2 == start_node:
            if node1 == end_node:
                return True
    return False


def link_edge(node1, node2, scene):
    for edge in scene.edges:
        start_node = edge.start_item
        end_node = edge.end_item
        if node1 == start_node:
            if node2 == end_node:
                return edge
        elif node2 == start_node:
            if node1 == end_node:
                return edge
    return None
