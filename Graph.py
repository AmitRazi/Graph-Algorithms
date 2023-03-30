import GraphEdge
import GraphNode


class Graph:
    def __init__(self):
        self.node_list = []
        self.edge_list = []

    def add_node(self, x, y,id):
        node = GraphNode.Node(x,y,id)
        self.node_list.append(node)
        for node in self.node_list:
            print(node)

    def find_node_in_radius(self, x, y):
        for node in self.node_list:
            distance = (x - node.x) ** 2 + (y - node.y) ** 2
            print(f"Click: ({x}, {y}), Node: ({node.x}, {node.y}), Distance: {distance}, Radius^2: {node.radius ** 2}")
            if distance <= node.radius ** 2:
                node_id = node.id
                self.node_list.remove(node)
                return node_id
        return -1
