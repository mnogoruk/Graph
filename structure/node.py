class Node:

    def __init__(self, label=None):
        self._label = str(label)
        self.graph = None
        self.index = None

    @property
    def label(self):
        return str(self._label)

    def copy(self):
        return Node(self.label)

    def __str__(self):
        return self.label or self.index

    def __repr__(self):
        return self.__str__()

