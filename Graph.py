import GraphEdge
import GraphNode


class Graph:
    def __init__(self):
        self.node_list = []
        self.edge_list = []

    def add_node(self, circle_id, x, y):
        node = GraphNode.Node(x, y, circle_id)
        self.node_list.append(node)
        for node in self.node_list:
            print(node)

    def add_edge(self, source_id, dest_id, edge_id):
        source_node = None
        dest_node = None
        for node in self.node_list:
            if node.circle_id == source_id:
                source_node = node
            elif node.circle_id == dest_id:
                dest_node = node
        if source_node is None or dest_node is None:
            return
        edge = GraphEdge.Edge(source_node.circle_id, dest_node.circle_id, edge_id)
        self.edge_list.append(edge)
        for edge in self.edge_list:
            print(edge)

    def delete_node(self, node_id):
        for node in self.node_list:
            if node.circle_id == node_id:
                edges_to_remove = []
                for edge in self.edge_list:
                    if edge.source == node_id or edge.dest == node_id:
                        edges_to_remove.append(edge)

                for edge in edges_to_remove:
                    self.edge_list.remove(edge)

                edge_ids = [edge.id for edge in edges_to_remove]
                self.node_list.remove(node)

                return edge_ids
        return None

    def find_node_by_id(self, target_id):
        for node in self.node_list:
            if node.circle_id == target_id:
                return node.x, node.y
        return None

    def find_node_in_radius(self, x, y):
        for node in self.node_list:
            distance = (x - node.x) ** 2 + (y - node.y) ** 2
            if distance <= node.radius ** 2:
                node_id = node.circle_id
                return node_id
        return -1
