class GraphError(Exception):
    pass


class EdgeError(GraphError):
    pass


class NodeError(GraphError):
    pass


class NodeDoesNotBelongToGraph(NodeError):

    def __init__(self, node):
        self.message = f"Node '{node}' does not belong to graph."
        super().__init__(self.message)
