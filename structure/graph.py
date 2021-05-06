from copy import deepcopy
from typing import List
import numpy as np

from structure.edge import Edge
from structure.exceptions import EdgeError, NodeError, NodeDoesNotBelongToGraph, GraphError
from structure.node import Node


class DirectedGraph:
    directed = True

    @classmethod
    def from_dict(cls, d: dict):
        nodes = {}
        edges = []
        for node_label in d.keys():
            node = cls.node(label=node_label)
            nodes[node_label] = node
        copy_d = deepcopy(d)
        for node in copy_d.keys():
            for connected_node_data in d[node]:
                if connected_node_data:
                    dest_node, weight, directed, label = cls._parse_connection_data(connected_node_data)
                    edge = cls.edge(
                        node_source=nodes[node],
                        node_dest=nodes[dest_node],
                        weight=weight,
                        directed=directed,
                        label=label)
                    edges.append(edge)

        graph = cls.__new__(cls)
        graph.__init__(list(map(lambda x: nodes[x], nodes)), edges)
        return graph

    @classmethod
    def from_vertices_matrix(cls, matrix: np.ndarray):
        cls.check_vertices_matrix(matrix)

        nodes = []
        edges = []
        for count in range(matrix.shape[0]):
            nodes.append(cls.node(label=count))

        for row_index in range(matrix.shape[0]):
            for column_index in range(matrix.shape[1]):
                weight = matrix[row_index, column_index]
                if weight != 0:
                    edge = cls.edge(node_source=nodes[row_index], node_dest=nodes[column_index], weight=weight)
                    edges.append(edge)

        graph = cls.__new__(cls)
        graph.__init__(nodes, edges)
        return graph

    @classmethod
    def check_vertices_matrix(cls, matrix: np.ndarray):
        if matrix.ndim != 2:
            raise GraphError(f"Vertices matrix must be 2 dimensional.")
        if matrix.shape[0] != matrix.shape[1]:
            raise GraphError(f"Vertices matrix must be square matrix.")

    @classmethod
    def _parse_connection_data(cls, connected_node_data):
        connected_node_data = dict(enumerate(connected_node_data))
        dest_node = connected_node_data.get(0)
        weight = connected_node_data.get(1, 1)
        directed = connected_node_data.get(2, True)
        label = connected_node_data.get(3, weight)
        return dest_node, weight, directed, label

    @classmethod
    def node(cls, **kwargs):
        return Node(**kwargs)

    @classmethod
    def edge(cls, **kwargs):
        if not kwargs.get('directed', True):
            raise EdgeError(f"Edge for directed graph must be directed.")
        kwargs.setdefault('directed', True)
        return Edge(**kwargs)

    def __init__(self, nodes: List[Node] = None, edges: List[Edge] = None):
        self.index_count = 0
        self.size = 0
        self.nodes = []
        self.edges = []

        if nodes is not None:
            self.add_nodes(*nodes)
        if edges is not None:
            self.add_edges(*edges)

        self.vertices_matrix = self.build_vertices_matrix()

    def add_nodes(self, *nodes):
        for node in nodes:
            self.init_node(node)
            self.nodes.append(node)

    def add_edges(self, *edges):
        for edge in edges:
            self.init_edge(edge)

    def init_edge(self, edge):
        self.check_edge(edge)
        self.edges.append(edge)

    def init_node(self, node):
        self.check_node(node)
        self.set_index_to_node(node)
        node.graph = self
        self.size = self.index_count

    def set_index_to_node(self, node):
        node.index = self.index_count
        self.index_count += 1

    def check_node(self, node):
        if node.graph != self and node.graph is not None:
            raise NodeError(f"Node '{node}' belongs to another graph.")

    def check_edge(self, edge):
        if edge.node_source not in self.nodes:
            raise NodeDoesNotBelongToGraph(edge.node_source)
        if edge.node_dest not in self.nodes:
            raise NodeDoesNotBelongToGraph(edge.node_dest)
        if not edge.directed:
            raise EdgeError(f"Edge for directed graph must be directed.")

    def build_vertices_matrix(self):
        matrix = np.zeros(shape=(self.size, self.size))
        for edge in self.edges:
            matrix[edge.node_source.index, edge.node_dest.index] = edge.weight
        return matrix

    def get_destination_nodes(self, source_node):
        source_index = self.get_index_of_node(source_node)
        row = self.vertices_matrix[source_index]
        nodes = []
        for index in range(len(row)):
            if row[index] != 0 and row[index] != np.inf:
                nodes.append(self.nodes[index])
        return nodes

    def get_source_nodes(self, destination_node):
        dest_index = self.get_index_of_node(destination_node)
        column = self.vertices_matrix[:, dest_index]
        nodes = []
        for index in range(len(column)):
            if column[index] != 0 and column[index] != np.inf:
                nodes.append(self.nodes[index])
        return nodes

    def get_edges_of_source_node(self, source_node):
        edges = []
        for edge in self.edges:
            if edge.node_source == source_node:
                edges.append(edge)
        return edges

    def get_edges_of_destination_node(self, destination_node):
        edges = []
        for edge in self.edges:

            if edge.node_dest == destination_node:
                edges.append(edge)

        return edges

    def get_index_of_node(self, node):
        if isinstance(node, int):
            index = node
        elif isinstance(node, Node):
            if node.graph != self:
                raise NodeDoesNotBelongToGraph(node)
            index = node.index
        else:
            raise NodeError("node must be instance of int or Node")
        return index


class Graph(DirectedGraph):
    directed = False

    @classmethod
    def from_vertices_matrix(cls, matrix: np.ndarray):
        cls.check_vertices_matrix(matrix)

        nodes = []
        edges = []
        for count in range(matrix.shape[0]):
            nodes.append(cls.node(label=count))

        for row_index in range(matrix.shape[0]):
            for column_index in range(row_index, matrix.shape[1]):
                weight = matrix[row_index, column_index]
                if weight != 0:
                    edge = cls.edge(node_source=nodes[row_index], node_dest=nodes[column_index], weight=weight)
                    edges.append(edge)

        graph = cls.__new__(cls)
        graph.__init__(nodes, edges)
        return graph

    @classmethod
    def check_vertices_matrix(cls, matrix: np.ndarray):
        super().check_vertices_matrix(matrix)
        size = matrix.shape[0]
        for row in range(size):
            for column in range(row, size):
                if matrix[row, column] != matrix[column, row]:
                    raise GraphError(f"matrix must be --''--.")

    @classmethod
    def _parse_connection_data(cls, connected_node_data):
        dest_node, weight, directed, label = super()._parse_connection_data(connected_node_data)
        return dest_node, weight, False, label

    @classmethod
    def edge(cls, **kwargs):
        if kwargs.get('directed', False):
            raise EdgeError(f"Edge for not directed graph must not be directed.")
        kwargs.setdefault('directed', False)
        return Edge(**kwargs)

    def check_edge(self, edge):
        if edge.node_source not in self.nodes:
            raise NodeDoesNotBelongToGraph(edge.node_source)
        if edge.node_dest not in self.nodes:
            raise NodeDoesNotBelongToGraph(edge.node_dest)
        if edge.directed:
            raise EdgeError(f"Edge for not directed graph must not be directed.")

    def get_connected_nodes(self, node):
        return super().get_source_nodes(node)

    def get_connected_edges(self, node):
        edges = set.union(
            set(super().get_edges_of_destination_node(node)),
            set(super(Graph, self).get_edges_of_source_node(node))
        )
        return list(edges)

    def get_source_nodes(self, destination_node):
        return self.get_connected_nodes(destination_node)

    def get_destination_nodes(self, source_node):
        return self.get_connected_nodes(source_node)

    def get_edges_of_destination_node(self, node):
        return self.get_connected_edges(node)

    def get_edges_of_source_node(self, source_node):
        return self.get_connected_edges(source_node)
