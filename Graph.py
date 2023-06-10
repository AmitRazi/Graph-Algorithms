from GraphEdge import Edge
from GraphNode import Node
from typing import List, Set


class Graph:
    """
    The Graph class represents a mathematical graph structure.
    It contains a list of nodes (node_list) and a list of edges (edge_list)
    that connect the nodes in the graph.
    """

    def __init__(self, gui):
        """
        Initializes a graph object with an empty list of nodes and edges, and a reference to a graphical user interface (GUI).

        :param gui: A graphical user interface for visualizing the graph.
        """
        self.node_list: List[Node] = []  # List of all nodes in the graph
        self.edge_list: List[Edge] = []  # List of all edges in the graph
        self.gui = gui  # Graphical user interface for visualizing the graph

    def find_node_by_id_coords(self, target_id):
        for node in self.node_list:
            if node.circle_id == target_id:
                return node.x, node.y
        return None

    def find_node_by_id(self, target_id):
        for node in self.node_list:
            if node.circle_id == target_id:
                return node
        return None

    def add_node(self, circle_id, x, y, scale=1.0):
        """
        Adds a new node to the graph.

        :param circle_id: Unique identifier for the node.
        :param x: x-coordinate of the node.
        :param y: y-coordinate of the node.
        :param scale: Size scale factor of the node.
        """
        node = Node(x, y, circle_id)  # Create new node
        node._radius = 20 * scale  # Set radius of the node according to scale
        self.node_list.append(node)  # Add node to the list of nodes

    def add_edge(self, source_id, dest_id, edge_id):
        """
        Adds an edge between two nodes in the graph.

        :param source_id: The identifier of the source node.
        :param dest_id: The identifier of the destination node.
        :param edge_id: The unique identifier of the edge.
        """
        # Check if an edge already exists between the two nodes.
        # If it does, then do not add the edge and return.
        for edge in self.edge_list:
            if (edge.source == source_id and edge.dest == dest_id) or (
                    edge.dest == source_id and edge.source == dest_id):
                return

        # Find the source and destination nodes in the node list.
        source_node = None
        dest_node = None
        for node in self.node_list:
            if node.circle_id == source_id:
                source_node = node
            elif node.circle_id == dest_id:
                dest_node = node

        # If either node was not found, then return without adding the edge.
        if source_node is None or dest_node is None:
            return

        # Add each node as a neighbor to the other.
        source_node.add_neighbor(dest_node)
        dest_node.add_neighbor(source_node)

        # Create a new edge and add it to the edge list.
        edge = Edge(source_node, dest_node, edge_id)
        self.edge_list.append(edge)

    def delete_node(self, node_id: Node):
        """
        Deletes a node from the graph, along with any edges connected to it.

        :param node_id: The identifier of the node to delete.
        :return: A list of the identifiers of the edges that were deleted, or None if the node was not found.
        """
        # Find the node in the node list.
        for node in self.node_list:
            if node.circle_id == node_id:
                # Inform the node's neighbors that it is being deleted.
                node.inform_neighbors()

                # Find all edges connected to the node.
                edges_to_remove = []
                for edge in self.edge_list:
                    if edge.source.circle_id == node_id or edge.dest.circle_id == node_id:
                        edges_to_remove.append(edge)

                # Remove the edges from the edge list.
                for edge in edges_to_remove:
                    self.edge_list.remove(edge)

                # Get a list of the identifiers of the removed edges.
                edge_ids = [edge.id for edge in edges_to_remove]

                # Remove the node from the node list.
                self.node_list.remove(node)

                # Return the identifiers of the removed edges.
                return edge_ids
        return None

    def delete_graph(self):
        if len(self.node_list) == 0:
            return
        """
        Deletes the entire graph, including all nodes and edges.
        """
        while self.node_list:
            for node in self.node_list:
                # Find the id of the node to delete
                id_to_delete = node.circle_id
                # Delete the node from the canvas
                self.gui.canvas.delete(id_to_delete)
                # Delete the node from the graph and get the list of edges to delete
                edge_list = self.gui.graph.delete_node(id_to_delete)
                # Delete each edge from the canvas
                for edge in edge_list:
                    self.gui.canvas.delete(edge)
        self.print_in_gui("Delete graph")

    def find_node_in_radius(self, x, y):
        """
        Finds a node within a specified radius.

        :param x: The x-coordinate to check.
        :param y: The y-coordinate to check.
        :return: The id of the node found within the radius, or -1 if no node is found.
        """
        for node in self.node_list:
            # Calculate the distance between the point and the node
            distance = (x - node.x) ** 2 + (y - node.y) ** 2
            # If the distance is within the node's radius, return the node's id
            if distance <= node.radius ** 2:
                return node.circle_id
        # No node was found within the radius
        return -1

    def find_edge(self, source_id, dest_id):
        """
        Finds an edge between two nodes.

        :param source_id: The id of the source node.
        :param dest_id: The id of the destination node.
        :return: The edge between the two nodes, or None if no edge exists.
        """
        for edge in self.edge_list:
            if (edge.source.circle_id == source_id and edge.dest.circle_id == dest_id) or (
                    edge.dest.circle_id == source_id and edge.source.circle_id == dest_id):
                return edge

    def color_edge(self, edge: Edge, color: str):
        """
        Colors an edge.

        :param edge: The edge to color.
        :param color: The color to use.
        """
        self.gui.color_edge(edge.id, color)

    def color_node(self, node: Node, color: str):
        """
        Colors a node.

        :param node: The node to color.
        :param color: The color to use.
        """
        self.gui.color_node(node.circle_id, color)

    def color_node_outline(self, node: Node, color: str):
        """
        Colors the outline of a node.

        :param node: The node whose outline to color.
        :param color: The color to use.
        """
        self.gui.color_node_outline(node.circle_id, color)

    def direct_graph(self, matching: Set[Edge]):
        """
        Directs the graph according to a given matching.

        :param matching: The matching to use to direct the graph.
        """
        self.gui.direct_graph(matching, self.edge_list)

    def print_in_gui(self, string: str):
        self.gui.print_to_gui(string)
