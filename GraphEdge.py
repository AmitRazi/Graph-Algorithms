import GraphNode


class Edge:
    def __init__(self, source_node, dest_node, direction):
        self._source = source_node
        self.dest = dest_node
        self.bi_direction = direction
