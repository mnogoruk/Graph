from structure.graph import DirectedGraph
from structure.node import Node


class DepthSearch:

    def __init__(self, graph):
        self.graph = graph
        self.visited_vertices = None
        self.found = False

    def _search(self, source: Node, destination: Node):

        for edge in self.graph.get_edges_of_destination_node(source):
            if destination == edge.node_dest:
                self.visited_vertices.append(destination)
                self.found = True
                return

            if edge.node_dest not in self.visited_vertices:
                self.visited_vertices.append(edge.node_dest)
                self._search(edge.node_dest, destination)
                if self.found:
                    return

    def search(self, source, destination):
        self.visited_vertices = [source]
        self._search(source, destination)
        return self.visited_vertices
