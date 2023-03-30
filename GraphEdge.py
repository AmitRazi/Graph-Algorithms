import GraphNode


class Edge:
    def __init__(self, source_node, dest_node, edge_id):
        self._source = source_node
        self._dest = dest_node
        self._id = edge_id

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, new_source):
        self._source = new_source

    @property
    def dest(self):
        return self._dest

    @dest.setter
    def dest(self, new_dest):
        self.dest = new_dest

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        self._id = new_id

    def swap(self):
        temp = self._source
        self.source = self.dest
        self.dest = temp

    def __str__(self):
        return f"{self.source, self.dest}"
