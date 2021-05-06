from structure.node import Node


class Edge:

    def __init__(self, node_source: Node, node_dest: Node, weight=1, label=None, directed=True):
        self.node_source = node_source
        self.node_dest = node_dest
        self.weight = float(weight)
        self.directed = directed
        if label is None:
            self._label = self.weight
        else:
            self._label = label

    @property
    def label(self):
        return str(self._label)

    def contains_by_index(self, index):
        return self.node_dest.index == index or self.node_source.index == index

    def __contains__(self, node):
        return self.node_dest == node or self.node_source == node

    def __str__(self):
        return self.label

    def __repr__(self):
        if self.directed:
            return f"Edge: ({self.label}, {self.node_source} -> {self.node_dest}: {self.weight})"
        else:
            return f"Edge: ({self.label}, {self.node_source} <-> {self.node_dest}: {self.weight})"

