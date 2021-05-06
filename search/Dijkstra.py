from math import inf
from structure.graph import Graph


class DijkstraSearch:

    def __init__(self, graph: Graph, source):
        self.graph = graph
        self.source = source
        self.vertex_marks = [[inf, [source]] for _ in range(self.graph.size)]
        self.vertex_marks[source.index][0] = 0
        self.queue = [source]
        self.searched = False
        self.visited_nodes = []

    def _search_paths(self):
        while self.queue:
            node = self.queue.pop(0)
            sorted_by_weight_nodes = sorted(self.graph.get_edges_of_source_node(node), key=lambda x: x.weight)
            for edge in sorted_by_weight_nodes:
                if edge.node_dest in self.visited_nodes:
                    continue
                path_length = self.vertex_marks[node.index][0] + edge.weight

                if path_length < self.vertex_marks[edge.node_dest.index][0]:
                    self.vertex_marks[edge.node_dest.index][0] = path_length
                    self.vertex_marks[edge.node_dest.index][1] = [*self.vertex_marks[node.index][1], edge.node_dest]
                    self.queue.append(edge.node_dest)
                self.visited_nodes.append(node)
        self.searched = True

    def search(self, destination):
        if not self.searched:
            self._search_paths()
        path = self.vertex_marks[destination.index]
        return path[1], path[0]
