import graphviz as gv


class Visualizer:
    index = 0

    def __init__(self, graph):
        self.__class__.index += 1
        self.graph = graph
        self.drawer_graph = None

    def visualize(self):
        if self.drawer_graph is None:
            self._build_drawer_graph()
        self.drawer_graph.view()

    def _build_drawer_graph(self):
        if self.graph.directed:
            self.drawer_graph = gv.Digraph(str(self.index))
        else:
            self.drawer_graph = gv.Graph(str(self.index))

        self.drawer_graph.attr('node', shape='circle')
        self._draw_edges()

    def _draw_edges(self):
        for node in self.graph.nodes:
            self.drawer_graph.node(node.label)

        for edge in self.graph.edges:
            self.drawer_graph.edge(edge.node_source.label, edge.node_dest.label, label=edge.label)
