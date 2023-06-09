from GraphNode import Node
import Graph
from GraphEdge import Edge
from typing import Dict, Set, List
import time


class GAlgorithm:
    # Initialize the graph algorithm with a graph
    def __init__(self, graph):
        self.graph = graph

    # Checks if a graph is bipartite using Breadth-first search
    def is_bipartite(self):
        """
        Checks whether a graph is bipartite. A graph is bipartite if its nodes can be divided
        into two groups such that all edges go from a node in one group to a node in the other group.

        :return: True if the graph is bipartite, False otherwise.
        """
        node_list = self.graph.node_list
        uncolored, red, blue = 0, 1, 2

        # Initialize all nodes to uncolored
        node_colors = {node: uncolored for node in node_list}

        # For each uncolored node, try to color it and its neighbors in alternating colors.
        for node in node_list:
            if node_colors[node] == uncolored:
                if not self._bfs_coloring(node, node_colors):
                    return False

        # If successfully colored, tag the nodes as per their color
        self._tag(node_colors)
        return True

    # Color the nodes and its neighbors in BFS fashion. If found a neighbor with the same color, return False.
    def _bfs_coloring(self, node: Node, node_colors: Dict[Node, int]) -> bool:
        """
        Colors nodes in BFS fashion, alternating between two colors. If a neighbor has the same color,
        it indicates the graph is not bipartite.

        :param node: Node from which BFS starts.
        :param node_colors: Dictionary to store color assignments for each node.
        :return: True if the nodes can be colored such that no two adjacent nodes have the same color,
                 False otherwise.
        """
        node_colors[node] = 1
        queue = [node]

        while queue:
            current = queue.pop(0)

            for neighbor in current.neighbors:
                if node_colors[neighbor] == 0:
                    node_colors[neighbor] = 3 - node_colors[current]
                    queue.append(neighbor)
                elif node_colors[neighbor] == node_colors[current]:
                    return False
        return True

    # Tag the nodes with 'A' or 'B' based on the color assigned
    def _tag(self, node_colors: Dict[Node, int]):
        """
        Tags the nodes with 'A' or 'B' based on the color assigned. This forms the two groups of a bipartite graph.

        :param node_colors: Dictionary with color assignments for each node.
        """
        for node, color in node_colors.items():
            if color == 1:
                node.group = 'A'
            else:
                node.group = 'B'

    def hungarian_algorithm(self, delay: int):
        """
        Executes the Hungarian Algorithm which is also known as Kuhn-Munkres Algorithm.
        It is used to find the maximum matching in a bipartite graph which in turn helps
        to solve the assignment problem. The algorithm guarantees to find the optimum solution
        for the assignment problem.

        :param delay: Time delay (in seconds) between operations for better visualization.
        :return: True if the graph is bipartite, False otherwise.
        """
        # Ensure the graph is bipartite before processing
        if not self.is_bipartite():
            return False

        # Initialize data structures
        node_list: List[Node] = self.graph.node_list
        group_b = {node for node in node_list if node.group == 'B'}
        matching = set()  # Tracks the current matching
        nodes_in_matching = set()  # Tracks the nodes involved in the matching

        # Orient the graph properly for the matching algorithm
        self._direct_graph(matching)

        # Main loop of the algorithm
        while True:
            flag = False
            for node in node_list:
                if node not in nodes_in_matching and node.group == 'A':
                    candidate_matching = self.find_augmenting_path_bfs(node, group_b.difference(nodes_in_matching))
                    if candidate_matching is None:
                        continue

                    # Filter out edges from the current matching that are in the augmenting path
                    filtered = set()
                    for edge in matching:
                        if edge not in candidate_matching:
                            filtered.add(edge)
                        else:
                            nodes_in_matching.remove(edge.source)
                            nodes_in_matching.remove(edge.dest)

                    # Update the matching with the augmenting path
                    self.color_path(candidate_matching, matching)
                    time.sleep(delay)
                    candidate_matching = set(candidate_matching[::2])
                    matching = filtered.union(candidate_matching)
                    self._direct_graph(matching)
                    self.color_matching(matching)
                    for edge in matching:
                        nodes_in_matching.add(edge.source)
                        nodes_in_matching.add(edge.dest)
                    time.sleep(delay)
                    flag = True
            if flag is False:
                break

        self.color_matching(matching)
        return True

    def color_matching(self, matching: set[Node]):
        """Colors the edges in the matching set to red and the others to black."""
        for edge in self.graph.edge_list:
            # If edge is part of the matching, color it red
            if edge in matching:
                self.graph.color_edge(edge, 'red')
            # Else color it black
            else:
                self.graph.color_edge(edge, 'black')

    def color_path(self, path: Set[Edge], matching: set[Edge]):
        """
        Colors the edges according to their current status.
        Blue: Edges in the augmenting path but not in the matching.
        Yellow: Edges in both the augmenting path and the matching.
        Red: Edges in the matching but not in the augmenting path.
        Black: Edges not in the augmenting path or the matching.
        """
        for edge in self.graph.edge_list:
            # If edge is in the path but not in the matching, color it blue
            if edge in path and edge not in matching:
                self.graph.color_edge(edge, 'blue')
            # If edge is in both the path and the matching, color it yellow
            elif edge in matching and edge in path:
                self.graph.color_edge(edge, 'yellow')
            # If edge is in the matching but not in the path, color it red
            elif edge in matching and edge not in path:
                self.graph.color_edge(edge, 'red')
            # Else color it black
            else:
                self.graph.color_edge(edge, 'black')

    def find_augmenting_path_bfs(self, node: Node, end_group: Set[Node]):
        """
        Breadth-first search (BFS) to find an augmenting path from a node in group A to a node in group B
        which is not currently part of the matching.
        """
        visited = set()

        # Start BFS with the starting node and an empty path
        queue = [(node, list())]
        visited.add(node)

        max_path = []
        max_length = 0

        # BFS main loop
        while queue:
            # Get current node and the path to reach it
            current_node, path = queue.pop(0)

            # If the current node is in the end group, check if it forms a longer augmenting path
            if current_node in end_group:
                if len(path) > max_length:
                    max_path = path
                    max_length = len(path)

            # Visit the neighbors of the current node
            for neighbor in current_node.neighbors:
                if neighbor not in visited:
                    edge = self.graph.find_edge(current_node.circle_id, neighbor.circle_id)
                    if edge.dest is not neighbor:
                        continue
                    # Mark the neighbor as visited
                    visited.add(neighbor)
                    # Create a new path by appending the neighbor to the current path
                    new_path = path.copy()
                    new_path.append(edge)
                    queue.append((neighbor, new_path))

        # If no augmenting path is found, return None
        if not max_path:
            return None
        return max_path

    def _direct_graph(self, matching: Set[Edge]):
        """
        Adjusts the direction of the edges in the graph to facilitate the process of finding augmenting paths.
        Edges in the matching go from group B to group A, others go from group A to group B.
        """
        edge_list: List[Edge] = self.graph.edge_list

        for edge in edge_list:
            # If edge is in the matching
            if edge in matching:
                # If edge's source node belongs to group 'A', swap source and destination
                if edge.source.group == 'A':
                    edge.swap()
            # If edge is not in the matching
            elif edge.source.group == 'B':
                # Swap source and destination
                edge.swap()

        # Direct the graph using the matching
        self.graph.direct_graph(matching)

    def bfs_spanning_tree(self, node: Node):
        """
        Creates a spanning tree using a breadth-first search (BFS) starting from a given node.
        """
        visited = set()
        # Begin with a queue that only contains the starting node
        queue = [node]
        vertices_list = []

        while queue:
            vertex = queue.pop(0)
            # If the vertex has not been visited before
            if vertex not in visited:
                # Mark the vertex as visited
                visited.add(vertex)
                # Add the vertex to the vertices list
                vertices_list.append(vertex)
                # Add all neighbors of the vertex to the queue
                for node in vertex.neighbors:
                    if node not in visited:
                        queue.append(node)

        # Return list of visited vertices, forming a spanning tree
        return vertices_list

    def max_min_degree(self, graph: Graph):
        """
        Returns the nodes with the maximum and minimum degrees in the graph.
        """
        # Initialize min, max degree and corresponding nodes
        min_degree = len(graph.node_list[0].neighbors)
        max_degree = len(graph.node_list[0].neighbors)
        min_node = graph.node_list[0]
        max_node = graph.node_list[0]
        # Loop over all nodes in graph
        for node in graph.node_list:
            neighborhood = len(node.neighbors)
            # If node's degree is smaller than current min, update min and min_node
            if neighborhood < min_degree:
                min_degree = neighborhood
                min_node = node
            # If node's degree is larger than current max, update max and max_node
            if neighborhood > max_degree:
                max_degree = neighborhood
                max_node = node

        # Return nodes with maximum and minimum degree
        return max_node, min_node

    def index_to_rgb(self, index: int) -> str:
        """
        Converts an index to an RGB color value.
        """
        r = (index * 50) % 256
        g = (index * 100) % 256
        b = (index * 150) % 256
        return '#%02x%02x%02x' % (r, g, b)

    def greedy_coloring(self, vertices_list: List[Node], delay: int):
        """
        Applies the greedy coloring algorithm to the graph.
        It colors the vertices in the order they appear in the vertices list.
        """
        max_color_index = 0
        for v in vertices_list:
            if v.color == -1:  # If the vertex is not colored yet
                available_colors = set(range(max_color_index + 1))  # Define the available colors

                for neighbor in v.neighbors:  # Check the neighbors of the vertex
                    if neighbor.color in available_colors:  # If a color is used by a neighbor, remove it from the available colors
                        available_colors.remove(neighbor.color)

                if not available_colors:  # If no colors are available
                    max_color_index = max_color_index + 1  # Add a new color
                    v.color = max_color_index  # Assign the new color to the vertex
                    tkinter_color = self.index_to_rgb(max_color_index)  # Convert the color to tkinter color
                    self.graph.color_node(v, tkinter_color)  # Apply the color
                else:  # If there are available colors
                    min_available_color_index = min(available_colors)  # Choose the smallest color
                    v.color = min_available_color_index  # Assign the color to the vertex
                    tkinter_color = self.index_to_rgb(min_available_color_index)  # Convert the color to tkinter color
                    self.graph.color_node(v, tkinter_color)  # Apply the color
            time.sleep(delay)  # Sleep for the defined delay

    def dfs_vertex_cut(self, v: Node, discovery: Dict[Node, int], low: Dict[Node, int], parent: Dict[Node, Node],
                       articulation_point: Dict[Node, bool], vertex_list: List[Node], time_: int):
        """
        Applies Depth-first Search (DFS) to find cut vertices (also known as articulation points) in the graph.
        """
        discovery[v] = low[v] = time_  # Initialize discovery and low time of v
        time_ += 1
        children = 0  # Initialize child counter

        for u in v.neighbors:  # For each neighbor u of v
            if discovery[u] == -1:  # If u is not visited yet, then recur for it
                children += 1
                parent[u] = v
                time_ = self.dfs_vertex_cut(u, discovery, low, parent, articulation_point, vertex_list, time_)
                low[v] = min(low[v],
                             low[u])  # Check if the subtree rooted with u has a connection to one of the ancestors of v

                if parent[
                    v] is None and children > 1:  # If v is not root and low value of one of its child is more than discovery value of v
                    articulation_point[v] = True
                elif parent[v] is not None and low[u] >= discovery[
                    v]:  # If v is not root and low value of one of its child is more than discovery value of v
                    articulation_point[v] = True

            elif u != parent[v]:  # Update low value of v for parent function calls.
                low[v] = min(low[v], discovery[u])

        return time_

    def tarjan_algorithm_cut_vertex(self, vertex_list: List[Node]):
        """
        Implements Tarjan's algorithm to find cut vertices in the graph.
        """
        discovery = {vertex: -1 for vertex in vertex_list}  # Initialize lists
        low = {vertex: -1 for vertex in vertex_list}
        parent = {vertex: None for vertex in vertex_list}
        articulation_point = {vertex: False for vertex in vertex_list}

        time_ = 0
        for vertex in vertex_list:  # Do DFS traversal
            if discovery[vertex] == -1:
                time_ = self.dfs_vertex_cut(vertex, discovery, low, parent, articulation_point, vertex_list, time_)

        for node, is_articulation_point in articulation_point.items():  # Check if vertex is an articulation point
            if is_articulation_point:
                return node
        return None

    def connected_components(self, cut_vertex: Node):
        """
        Returns the connected components of the graph after removing a cut vertex.
        """
        visited = set()  # Initialize list of visited nodes
        components = []  # Initialize list of components

        for v in cut_vertex.neighbors:  # For each neighbor of the cut vertex
            if v not in visited:  # If it hasn't been visited yet
                component = []  # Initialize a new component
                stack = [v]

                while stack:  # While there are nodes in the stack
                    vertex = stack.pop()  # Remove a node from the stack
                    if vertex not in visited:  # If it hasn't been visited yet
                        visited.add(vertex)  # Mark it as visited
                        component.append(vertex)  # Add it to the current component

                        for neighbor in vertex.neighbors:  # For each of its neighbors
                            if neighbor != cut_vertex:  # If the neighbor is not the cut vertex
                                stack.append(neighbor)  # Add it to the stack

                component.append(cut_vertex)  # Add the cut vertex to the component
                components.append(component)  # Add the component to the list of components

        return components

    def component_spanning_tree(self, component_vertex_list: List[Node], cut_vertex: Node, delay: int):
        """
        Creates a spanning tree for each connected component in the graph after removing a cut vertex.
        """
        queue = [cut_vertex]  # Initialize queue with the cut_vertex
        spanning_tree = []  # Initialize empty list for the spanning tree
        visited = set()  # Set to keep track of visited nodes
        ancestors = {cut_vertex: None}  # Dictionary to store ancestors of each node

        while queue:  # Process until queue is empty
            vertex = queue.pop(0)  # Get a vertex from the queue
            if vertex not in visited:  # If the vertex hasn't been visited yet
                visited.add(vertex)  # Mark it as visited
                if vertex != cut_vertex:  # If it's not the cut vertex
                    edge = self.graph.find_edge(vertex.circle_id, ancestors[vertex].circle_id)
                    self.graph.color_edge(edge, "Red")  # Color the edge to the ancestor
                    time.sleep(delay)  # Wait for a delay to allow visualization
                spanning_tree.append(vertex)  # Add the vertex to the spanning tree
                for node in vertex.neighbors:  # For each of its neighbors
                    if node in component_vertex_list and node not in visited:  # If the neighbor is in the same component and hasn't been visited
                        ancestors[node] = vertex  # Set the current vertex as the ancestor
                        queue.append(node)  # Add the neighbor to the queue
        return spanning_tree  # Return the spanning tree

    def combine_coloring(self, spanning_tree_1: List[Node], spanning_tree_2: List[Node], cut_vertex: Node):
        """
        Combines the colorings of the two connected components at the cut vertex.
        """
        # If both spanning trees start with the same color, no need to combine coloring
        if spanning_tree_1[0].color == spanning_tree_2[0].color:
            return

        # Change color of the node in the first tree that matches the color of the root of the second tree
        for node in spanning_tree_1:
            if node.color == spanning_tree_2[0].color and node in spanning_tree_2[0].neighbors:
                node.color, spanning_tree_2[0].color = spanning_tree_2[0].color, node.color

    def find_triad(self, graph: Graph):
        """
        Finds a triad in the graph - three nodes where two of them are connected to a common node but not to each other.
        """
        for x in graph.node_list:  # Iterate over all nodes in the graph
            for y in x.neighbors:  # Iterate over neighbors of a given node
                for z in x.neighbors:  # Again, iterate over neighbors of the same node
                    # If y and z are different and z is not a neighbor of y, then we found a triad
                    if y != z and z not in y.neighbors:
                        self.graph.color_node_outline(x, "Green")  # Color the nodes of the triad
                        self.graph.color_node_outline(y, "Blue")
                        self.graph.color_node_outline(z, "Yellow")
                        return x, y, z  # Return the nodes of the triad

    def triad_bfs(self, vertex_list: List[Node], x: Node, y: Node, z: Node, delay: int):
        """
        Creates a spanning tree that includes a given triad using a breadth-first search (BFS).
        """
        queue = [x]  # Initialize the queue with the first node of the triad
        spanning_tree = []  # Initialize empty list for the spanning tree
        visited = set()  # Set to keep track of visited nodes
        ancestor = x  # Set the ancestor as the first node of the triad

        while queue:  # Process until queue is empty
            vertex = queue.pop(0)  # Get a vertex from the queue
            if vertex not in visited:  # If the vertex hasn't been visited yet
                visited.add(vertex)  # Mark it as visited
                # If vertex is not the second or third node of the triad
                if vertex != y and vertex != z:
                    spanning_tree.append(vertex)  # Add the vertex to the spanning tree
                    if vertex != x:  # If vertex is not the first node of the triad
                        edge = self.graph.find_edge(vertex.circle_id, ancestor.circle_id)
                        self.graph.color_edge(edge, "Red")  # Color the edge to the ancestor
                        time.sleep(delay)  # Wait for a delay to allow visualization
                # Add all unvisited neighbors (that are not the second or third node of the triad) to the queue
                for node in vertex.neighbors:
                    if node not in visited and node != y and node != z:
                        queue.append(node)
            ancestor = vertex  # Update the ancestor

        # Process the second and third nodes of the triad
        spanning_tree.append(y)
        edge = self.graph.find_edge(x.circle_id, y.circle_id)
        self.graph.color_edge(edge, "Red")
        time.sleep(delay)
        spanning_tree.append(z)
        edge = self.graph.find_edge(x.circle_id, z.circle_id)
        self.graph.color_edge(edge, "Red")
        time.sleep(delay)
        return spanning_tree  # Return the spanning tree

    def brooks_algorithm(self, graph: Graph, delay: int):
        """
        Implements Brooks' theorem to color the graph.
        The theorem states that every connected graph with maximum degree 'd' can be colored with 'd' colors.
        Exceptions: complete graphs and odd cycles.
        """
        max_degree, min_degree = self.max_min_degree(graph)  # Get the node with max and min degrees

        # If the min degree is less than the max degree, color using BFS starting from the node with min degree
        if len(min_degree.neighbors) < len(max_degree.neighbors):
            spanning_tree = self.bfs_spanning_tree(min_degree)[::-1]
            self.greedy_coloring(spanning_tree, delay)
            return

        # Find a cut vertex if it exists
        cut_vertex = self.tarjan_algorithm_cut_vertex(graph.node_list)
        if cut_vertex is not None:  # If there is a cut vertex
            self.graph.color_node(cut_vertex, "Red")  # Color the cut vertex
            components = self.connected_components(
                cut_vertex)  # Find the connected components after removing the cut vertex
            # Create spanning trees for each component and color them using the greedy algorithm
            spanning_tree_1 = self.component_spanning_tree(components[0], cut_vertex, delay)[::-1]
            spanning_tree_2 = self.component_spanning_tree(components[1], cut_vertex, delay)[::-1]
            self.greedy_coloring(spanning_tree_1, delay)
            self.greedy_coloring(spanning_tree_2, delay)
            self.combine_coloring(spanning_tree_1, spanning_tree_2,
                                  cut_vertex)  # Combine the colorings at the cut vertex
            return

        # If there is no cut vertex,find a triad of vertices such that two are unconnected
        x, y, z = self.find_triad(graph)
        spanning_tree = self.triad_bfs(graph.node_list, x, y, z, delay)[::-1]
        self.greedy_coloring(spanning_tree, delay)
