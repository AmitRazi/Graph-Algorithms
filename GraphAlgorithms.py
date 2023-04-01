from GraphNode import Node
import Graph
from GraphEdge import Edge
from typing import Dict, Set, List
import time


class GAlgorithm:
    def __init__(self, graph):
        self.graph = graph

    def is_bipartite(self):
        print("in tag")
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

    def hungarian_algorithm(self,delay: int):
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

                    candidate_matching = candidate_matching[::2]
                    candidate_matching_set = set(candidate_matching)
                    matching = filered_matching.union(candidate_matching_set)
                    self.color_path(candidate_matching,matching)

                    self._direct_graph(matching)
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
                self.graph.color_edge(edge,'red')
            else:
                self.graph.color_edge(edge,'black')

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

    def find_augmenting_path_bfs(self, node: Node, end_group: Set[Node]) -> Set:
        visited = set()

        queue = [(node, list())]
        visited.add(node)

        while queue:
            current_node, path = queue.pop(0)

            for node in end_group:
                if node == current_node:
                    return path

            for neighbor in current_node.neighbors:
                if neighbor not in visited:
                    edge = self.graph.find_edge(current_node.circle_id, neighbor.circle_id)
                    if edge.dest is not neighbor:
                        continue
                    visited.add(neighbor)
                    new_path = path.copy()
                    new_path.append(edge)
                    queue.append((neighbor, new_path))

        return None

    def _direct_graph(self, matching: Set[Edge]):
        edge_list: List[Edge] = self.graph.edge_list

        for edge in edge_list:
            if edge in matching:
                if edge.source.group == 'A':
                    edge.swap()

            elif edge.source.group == 'B':
                edge.swap()

        self.graph.direct_graph(matching)
