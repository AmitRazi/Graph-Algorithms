from GraphEdge import Edge
from GraphNode import Node
from typing import List, Set


class Graph:
    def __init__(self, gui):
        self.node_list: List[Node] = []
        self.edge_list: List[Edge] = []
        self.gui = gui

    def add_node(self, circle_id, x, y, scale=1.0):
        node = Node(x, y, circle_id)
        node._radius = 20 * scale
        self.node_list.append(node)
        print(node)

    def add_edge(self, source_id, dest_id, edge_id):
        for edge in self.edge_list:
            if (edge.source == source_id and edge.dest == dest_id) or (
                    edge.dest == source_id and edge.source == dest_id):
                return
        source_node = None
        dest_node = None
        for node in self.node_list:
            if node.circle_id == source_id:
                source_node = node
            elif node.circle_id == dest_id:
                dest_node = node
        if source_node is None or dest_node is None:
            return
        source_node.add_neighbor(dest_node)
        dest_node.add_neighbor(source_node)
        edge = Edge(source_node, dest_node, edge_id)
        self.edge_list.append(edge)
        for edge in self.edge_list:
            print(edge)

    def delete_node(self, node_id: Node):
        for node in self.node_list:
            if node.circle_id == node_id:
                node.inform_neighbors()
                edges_to_remove = []
                for edge in self.edge_list:
                    if edge.source.circle_id == node_id or edge.dest.circle_id == node_id:
                        edges_to_remove.append(edge)

                for edge in edges_to_remove:
                    self.edge_list.remove(edge)
                edge_ids = [edge.id for edge in edges_to_remove]
                self.node_list.remove(node)

                return edge_ids
        return None

    def delete_graph(self):
        while self.node_list:
            for node in self.node_list:
                id_to_delete = self.find_node_in_radius(node.x, node.y)
                self.gui.canvas.delete(id_to_delete)
                edge_list = self.gui.graph.delete_node(id_to_delete)
                for edge in edge_list:
                    self.gui.canvas.delete(edge)

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

    def find_edge(self, source_id, dest_id):
        for edge in self.edge_list:
            if (edge.source.circle_id == source_id and edge.dest.circle_id == dest_id) or (
                    edge.dest.circle_id == source_id and edge.source.circle_id == dest_id):
                return edge

    def color_edge(self, edge: Edge, color: str):
        self.gui.color_edge(edge.id, color)

    def color_node(self, node: Node, color: str):
        self.gui.color_node(node.circle_id, color)

    def color_node_outline(self, node: Node, color: str):
        self.gui.color_node_outline(node.circle_id, color)

    def direct_graph(self, matching: Set[Edge]):
        self.gui.direct_graph(matching, self.edge_list)
