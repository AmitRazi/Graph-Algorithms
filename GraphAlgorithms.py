from GraphNode import Node
import Graph
from GraphEdge import Edge
from typing import Dict, Set, List
import time


class GAlgorithm:
    def __init__(self, graph):
        self.graph = graph

    def is_bipartite(self):
        node_list = self.graph.node_list
        uncolored, red, blue = 0, 1, 2

        node_colors = {node: uncolored for node in node_list}

        for node in node_list:
            if node_colors[node] == uncolored:
                if not self._bfs_coloring(node, node_colors):
                    return False

        self._tag(node_colors)
        return True

    def _bfs_coloring(self, node: Node, node_colors: Dict[Node, int]) -> bool:
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

    def _tag(self, node_colors: Dict[Node, int]):

        for node, color in node_colors.items():
            if color == 1:
                node.group = 'A'
            else:
                node.group = 'B'

    def hungarian_algorithm(self, delay: int):
        if not self.is_bipartite():
            return False

        node_list: List[Node] = self.graph.node_list

        group_b = {node for node in node_list if node.group == 'B'}
        matching = set()
        nodes_in_matching = set()
        self._direct_graph(matching)
        while True:
            flag = False
            for node in node_list:
                if node not in nodes_in_matching and node.group == 'A':
                    candidate_matching = self.find_augmenting_path_bfs(node, group_b.difference(nodes_in_matching))
                    if candidate_matching is None:
                        continue

                    filered_matching = set()
                    for edge in matching:
                        if edge not in candidate_matching:
                            filered_matching.add(edge)
                        else:
                            nodes_in_matching.remove(edge.source)
                            nodes_in_matching.remove(edge.dest)

                    self.color_path(candidate_matching, matching)
                    time.sleep(delay)
                    candidate_matching = candidate_matching[::2]
                    candidate_matching_set = set(candidate_matching)
                    matching = filered_matching.union(candidate_matching_set)
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

    def color_matching(self, matching: Set[Node]):
        for edge in self.graph.edge_list:
            if edge in matching:
                self.graph.color_edge(edge, 'red')
            else:
                self.graph.color_edge(edge, 'black')

    def color_path(self, path: Set[Edge], matching: set[Edge]):
        for edge in self.graph.edge_list:
            if edge in path and edge not in matching:
                self.graph.color_edge(edge, 'blue')
            elif edge in matching and edge in path:
                self.graph.color_edge(edge, 'yellow')
            elif edge in matching and edge not in path:
                self.graph.color_edge(edge, 'red')
            else:
                self.graph.color_edge(edge, 'black')

    def find_augmenting_path_bfs(self, node: Node, end_group: Set[Node]):
        visited = set()

        queue = [(node, list())]
        visited.add(node)

        max_path = []
        max_length = 0

        while queue:
            current_node, path = queue.pop(0)

            if current_node in end_group:
                if len(path) > max_length:
                    max_path = path
                    max_length = len(path)

            for neighbor in current_node.neighbors:
                if neighbor not in visited:
                    edge = self.graph.find_edge(current_node.circle_id, neighbor.circle_id)
                    if edge.dest is not neighbor:
                        continue
                    visited.add(neighbor)
                    new_path = path.copy()
                    new_path.append(edge)
                    queue.append((neighbor, new_path))

        if not max_path:
            return None
        return max_path

    def _direct_graph(self, matching: Set[Edge]):
        edge_list: List[Edge] = self.graph.edge_list

        for edge in edge_list:
            if edge in matching:
                if edge.source.group == 'A':
                    edge.swap()

            elif edge.source.group == 'B':
                edge.swap()

        self.graph.direct_graph(matching)

    def bfs_spanning_tree(self, node: Node):
        visited = set()
        queue = [node]
        vertices_list = []

        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)
                vertices_list.append(vertex)
                for node in vertex.neighbors:
                    if node not in visited:
                        queue.append(node)

        return vertices_list

    def max_min_degree(self, graph: Graph):
        min_degree = len(graph.node_list[0].neighbors)
        max_degree = len(graph.node_list[0].neighbors)
        min_node = graph.node_list[0]
        max_node = graph.node_list[0]
        for node in graph.node_list:
            neighborhood = len(node.neighbors)
            if neighborhood < min_degree:
                min_degree = neighborhood
                min_node = node
            if neighborhood > max_degree:
                max_degree = neighborhood
                max_node = node

        return max_node, min_node

    def index_to_rgb(self, index: int) -> str:
        r = (index * 50) % 256
        g = (index * 100) % 256
        b = (index * 150) % 256
        return '#%02x%02x%02x' % (r, g, b)

    def greedy_coloring(self, vertices_list: List[Node], delay: int):
        max_color_index = 0
        for v in vertices_list:
            if v.color == -1:
                available_colors = set(range(max_color_index + 1))

                for neighbor in v.neighbors:
                    if neighbor.color in available_colors:
                        available_colors.remove(neighbor.color)

                if not available_colors:
                    max_color_index = max_color_index + 1
                    v.color = max_color_index
                    tkinter_color = self.index_to_rgb(max_color_index)
                    self.graph.color_node(v, tkinter_color)
                else:
                    min_available_color_index = min(available_colors)
                    v.color = min_available_color_index
                    tkinter_color = self.index_to_rgb(min_available_color_index)
                    self.graph.color_node(v, tkinter_color)
            time.sleep(delay)

    def dfs_vertex_cut(self, v: Node, discovery: Dict[Node, int], low: Dict[Node, int], parent: Dict[Node, Node],
                       articulation_point: Dict[Node, bool], vertex_list: List[Node], time_: int):
        discovery[v] = low[v] = time_
        time_ += 1
        children = 0

        for u in v.neighbors:
            if discovery[u] == -1:
                children += 1
                parent[u] = v
                time_ = self.dfs_vertex_cut(u, discovery, low, parent, articulation_point, vertex_list, time_)
                low[v] = min(low[v], low[u])

                if parent[v] is None and children > 1:
                    articulation_point[v] = True
                elif parent[v] is not None and low[u] >= discovery[v]:
                    articulation_point[v] = True

            elif u != parent[v]:
                low[v] = min(low[v], discovery[u])

        return time_

    def tarjan_algorithm_cut_vertex(self, vertex_list: List[Node]):
        discovery = {vertex: -1 for vertex in vertex_list}
        low = {vertex: -1 for vertex in vertex_list}
        parent = {vertex: None for vertex in vertex_list}
        articulation_point = {vertex: False for vertex in vertex_list}

        time_ = 0
        for vertex in vertex_list:
            if discovery[vertex] == -1:
                time_ = self.dfs_vertex_cut(vertex, discovery, low, parent, articulation_point, vertex_list, time_)

        for node, is_articulation_point in articulation_point.items():
            if is_articulation_point:
                return node
        return None

    def connected_components(self, cut_vertex: Node):
        visited = set()
        components = []

        for v in cut_vertex.neighbors:
            if v not in visited:
                component = []
                stack = [v]

                while stack:
                    vertex = stack.pop()
                    if vertex not in visited:
                        visited.add(vertex)
                        component.append(vertex)

                        for neighbor in vertex.neighbors:
                            if neighbor != cut_vertex:
                                stack.append(neighbor)

                component.append(cut_vertex)
                components.append(component)

        return components

    def component_spanning_tree(self, component_vertex_list: List[Node], cut_vertex: Node,delay:int):
        queue = [cut_vertex]
        spanning_tree = []
        visited = set()
        ancestors = {cut_vertex: None}
        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)
                if vertex != cut_vertex:
                    edge = self.graph.find_edge(vertex.circle_id, ancestors[vertex].circle_id)
                    self.graph.color_edge(edge, "Red")
                    time.sleep(delay)
                spanning_tree.append(vertex)
                for node in vertex.neighbors:
                    if node in component_vertex_list and node not in visited:
                        ancestors[node] = vertex
                        queue.append(node)
        return spanning_tree

    def combine_coloring(self, spanning_tree_1: List[Node], spanning_tree_2: List[Node], cut_vertex: Node):
        if spanning_tree_1[0].color == spanning_tree_2[0].color:
            return

        for node in spanning_tree_1:
            if node.color == spanning_tree_2[0].color and node in spanning_tree_2[0].neighbors:
                node.color, spanning_tree_2[0].color = spanning_tree_2[0].color, node.color

    def find_triad(self, graph: Graph):
        for x in graph.node_list:
            for y in x.neighbors:
                for z in x.neighbors:
                    if y != z and z not in y.neighbors:
                        self.graph.color_node_outline(x, "Green")
                        self.graph.color_node_outline(y, "Blue")
                        self.graph.color_node_outline(z, "Yellow")
                        return x, y, z

    def triad_bfs(self, vertex_list: List[Node], x: Node, y: Node, z: Node,delay:int):
        queue = [x]
        spanning_tree = []
        visited = set()
        ancestor = x
        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)
                if vertex != y and vertex != z:
                    spanning_tree.append(vertex)
                    if vertex != x:
                        edge = self.graph.find_edge(vertex.circle_id, ancestor.circle_id)
                        self.graph.color_edge(edge, "Red")
                        time.sleep(delay)
                for node in vertex.neighbors:
                    if node not in visited and node != y and node != z:
                        queue.append(node)
            ancestor = vertex
        spanning_tree.append(y)
        edge = self.graph.find_edge(x.circle_id, y.circle_id)
        self.graph.color_edge(edge, "Red")
        time.sleep(delay)
        spanning_tree.append(z)
        edge = self.graph.find_edge(x.circle_id, z.circle_id)
        self.graph.color_edge(edge, "Red")
        time.sleep(delay)
        return spanning_tree

    def brooks_algorithm(self, graph: Graph, delay: int):
        max_degree, min_degree = self.max_min_degree(graph)

        if len(min_degree.neighbors) < len(max_degree.neighbors):
            spanning_tree = self.bfs_spanning_tree(min_degree)[::-1]
            self.greedy_coloring(spanning_tree, delay)
            return

        cut_vertex = self.tarjan_algorithm_cut_vertex(graph.node_list)
        if cut_vertex is not None:
            self.graph.color_node(cut_vertex, "Red")
            components = self.connected_components(cut_vertex)
            spanning_tree_1 = self.component_spanning_tree(components[0], cut_vertex,delay)[::-1]
            spanning_tree_2 = self.component_spanning_tree(components[1], cut_vertex,delay)[::-1]
            self.greedy_coloring(spanning_tree_1, delay)
            self.greedy_coloring(spanning_tree_2, delay)
            self.combine_coloring(spanning_tree_1, spanning_tree_2, cut_vertex)
            return

        x, y, z = self.find_triad(graph)
        spanning_tree = self.triad_bfs(graph.node_list, x, y, z,delay)[::-1]
        self.greedy_coloring(spanning_tree, delay)
