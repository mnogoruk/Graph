from structure.graph import DirectedGraph
from structure.node import Node


class BreadthFirstSearch:

    def __init__(self, graph):
        self.graph = graph
        self.queue = None
        self.found = False

        self.distances = [None for _ in range(self.graph.size)]
        self.visited_vertices = [None for _ in range(self.graph.size)]
        self.path = None

    def search(self, source: Node, destination: Node):
        self.queue = [source]
        self.distances[source.index] = 0

        while self.queue:
            node = self.queue.pop(0)
            for edge in self.graph.get_edges_of_source_node(node):
                if self.distances[edge.node_dest.index] is None:
                    self.distances[edge.node_dest.index] = self.distances[edge.node_source.index] + 1
                    self.visited_vertices[edge.node_dest.index] = edge.node_source
                    self.queue.append(edge.node_dest)

        self.path = [destination]
        parent = self.visited_vertices[destination.index]

        while parent is not None:
            self.path.append(parent)
            parent = self.visited_vertices[parent.index]

        self.path = self.path[::-1]

        return self.path
