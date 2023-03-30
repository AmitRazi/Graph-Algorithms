class Node:
    def __init__(self, x, y,circle_id):
        self._circle_id = circle_id
        self._x = x
        self._y = y
        self._radius = 20
        self._color = 'blue'
        self._group = 'None'

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_x):
        self._x = new_x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new_y):
        self._y = new_y

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        self._color = new_color

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, new_group):
        self._group = new_group

    @property
    def circle_id(self):
        return self._circle_id

    @circle_id.setter
    def circle_id(self,new_id):
        self._circle_id = id

    @property
    def radius(self):
        return self._radius

    def __str__(self):
        return f"Node ID {self.circle_id}: ({self.x},{self.y})"
