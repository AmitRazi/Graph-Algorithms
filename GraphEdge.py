from GraphNode import Node


class Edge:
    """
    The Edge class represents an edge in a graph, connecting two nodes.
    """

    def __init__(self, source_node: Node, dest_node: Node, edge_id: int):
        """
        Initializes a new edge with a source node, destination node, and an id.

        :param source_node: The node where the edge starts.
        :param dest_node: The node where the edge ends.
        :param edge_id: The id of the edge.
        """
        self._source = source_node
        self._dest = dest_node
        self._id = edge_id

    @property
    def source(self) -> Node:
        """
        The source node of the edge.

        :return: The source node.
        """
        return self._source

    @source.setter
    def source(self, new_source):
        """
        Set a new source for the edge.

        :param new_source: The new source node.
        """
        self._source = new_source

    @property
    def dest(self):
        """
        The destination node of the edge.

        :return: The destination node.
        """
        return self._dest

    @dest.setter
    def dest(self, new_dest):
        """
        Set a new destination for the edge.

        :param new_dest: The new destination node.
        """
        self._dest = new_dest

    @property
    def id(self):
        """
        The id of the edge.

        :return: The id of the edge.
        """
        return self._id

    @id.setter
    def id(self, new_id):
        """
        Set a new id for the edge.

        :param new_id: The new id for the edge.
        """
        self._id = new_id

    def swap(self):
        """
        Swaps the source and destination nodes of the edge.
        """
        temp = self._source
        self.source = self.dest
        self.dest = temp

    def __str__(self):
        """
        Returns a string representation of the edge.

        :return: A tuple containing the string representations of the source and destination nodes.
        """
        return f"{self.source.__str__(), self.dest.__str__()}"
