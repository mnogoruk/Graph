from copy import deepcopy, copy

from structure.edge import Edge
from structure.graph import Graph


class Kruskal:
    class Archipelago:
        def __init__(self):
            self.islands = []

        def add(self, edge):

            for island_ind in range(len(self.islands)):
                for existing_edge in self.islands[island_ind]:
                    if edge.node_source in existing_edge or edge.node_source in existing_edge:
                        self.islands[island_ind].append(edge)
                        return

            else:
                self.islands.append([edge])

        def does_make_circle(self, edge):
            for island_ind in range(len(self.islands)):
                found = False
                for existing_edge in self.islands[island_ind]:
                    if edge.node_dest in existing_edge:
                        if found:
                            return True
                        found = True
                    if edge.node_source in existing_edge:
                        if found:
                            return True
                        found = True

            else:
                return False

        def connect(self, edge):
            connecting_islands = []
            for island_ind in range(len(self.islands)):
                for existing_edge in self.islands[island_ind]:
                    if edge.node_dest in existing_edge:
                        connecting_islands.append(island_ind)
                    elif edge.node_source in existing_edge:
                        connecting_islands.append(island_ind)
            try:
                island1 = self.islands[connecting_islands[0]]
                island2 = self.islands[connecting_islands[1]]
                island1.extend(island2)
                island1.append(edge)

                self.islands.pop(connecting_islands[1])

            except IndexError:
                pass

        def __contains__(self, edge):
            for island in self.islands:
                for edge in island:
                    if edge == edge:
                        return True
            else:
                return False

    def __init__(self, graph: Graph):
        self.input_graph = graph
        self.raw_nodes = [node.copy() for node in graph.nodes]
        self.raw_edges = [
            Edge(self.raw_nodes[edge.node_source.index], self.raw_nodes[edge.node_dest.index], edge.weight, edge.label,
                 edge.directed) for edge in graph.edges]
        self.sorted_edges = sorted(self.raw_edges, key=lambda x: x.weight)
        self.free_isolated_nodes = copy(self.raw_nodes)
        self.archipelago = Kruskal.Archipelago()

    def tree(self):
        self._first_iteration()
        self._second_iteration()
        return Graph(self.raw_nodes, self.archipelago.islands[0])

    def _first_iteration(self):

        for index, edge in enumerate(self.sorted_edges):
            cont = True
            if edge.node_source in self.free_isolated_nodes:
                self.free_isolated_nodes.pop(self.free_isolated_nodes.index(edge.node_source))
                cont = False
            if edge.node_dest in self.free_isolated_nodes:
                self.free_isolated_nodes.pop(self.free_isolated_nodes.index(edge.node_dest))
                cont = False

            if cont:
                continue

            self.sorted_edges.pop(index)
            self.archipelago.add(edge)

    def _second_iteration(self):
        for index, edge in enumerate(self.sorted_edges):
            if not self.archipelago.does_make_circle(edge):
                if len(self.archipelago.islands) > 1:
                    self.archipelago.connect(edge)
                else:
                    return
