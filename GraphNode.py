class Node:
    """
    The Node class represents a node in a graph, with certain attributes like coordinates, color, group, and neighbors.
    """

    def __init__(self, x, y, circle_id):
        """
        Initializes a new node with x and y coordinates, and an id.

        :param x: The x-coordinate of the node.
        :param y: The y-coordinate of the node.
        :param circle_id: The id of the node.
        """
        self._circle_id = circle_id
        self._x = x
        self._y = y
        self._radius = 20
        self._color = -1
        self._group = 'None'
        self.neighbors = []

    def add_neighbor(self, neighbor):
        """
        Adds a neighbor to this node.

        :param neighbor: The node to add as a neighbor.
        """
        self.neighbors.append(neighbor)

    def remove_neighbor(self, neighbor):
        """
        Removes a neighbor from this node.

        :param neighbor: The node to remove from the neighbors.
        """
        self.neighbors.remove(neighbor)

    def inform_neighbors(self):
        """
        Informs all neighbor nodes that they should remove this node from their list of neighbors.
        """
        for node in self.neighbors:
            node.remove_neighbor(self)

    @property
    def x(self):
        """
        The x-coordinate of the node.

        :return: The x-coordinate of the node.
        """
        return self._x

    @x.setter
    def x(self, new_x):
        """
        Sets a new x-coordinate for the node.

        :param new_x: The new x-coordinate.
        """
        self._x = new_x

    @property
    def y(self):
        """
        The y-coordinate of the node.

        :return: The y-coordinate of the node.
        """
        return self._y

    @y.setter
    def y(self, new_y):
        """
        Sets a new y-coordinate for the node.

        :param new_y: The new y-coordinate.
        """
        self._y = new_y

    @property
    def color(self):
        """
        The color of the node.

        :return: The color of the node.
        """
        return self._color

    @color.setter
    def color(self, new_color):
        """
        Sets a new color for the node.

        :param new_color: The new color.
        """
        self._color = new_color

    @property
    def group(self):
        """
        The group of the node.

        :return: The group of the node.
        """
        return self._group

    @group.setter
    def group(self, new_group):
        """
        Sets a new group for the node.

        :param new_group: The new group.
        """
        self._group = new_group

    @property
    def circle_id(self):
        """
        The id of the node.

        :return: The id of the node.
        """
        return self._circle_id

    @circle_id.setter
    def circle_id(self, new_id):
        """
        Sets a new id for the node.

        :param new_id: The new id for the node.
        """
        self._circle_id = new_id

    @property
    def radius(self):
        """
        The radius of the node.

        :return: The radius of the node.
        """
        return self._radius

    def __str__(self):
        """
        Returns a string representation of the node, with its id and coordinates.
        """
        return f"Node ID {self.circle_id}: ({self.x},{self.y})"
