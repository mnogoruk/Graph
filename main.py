from copy import deepcopy

import numpy as np
from graphviz import Digraph

from algorithm.Kruskal import Kruskal
from search.Dijkstra import DijkstraSearch
from search.breadth import BreadthFirstSearch
from search.depth import DepthSearch
from structure.edge import Edge
from structure.graph import DirectedGraph, Graph
from structure.node import Node
from view.visualization import Visualizer


def main():
    v_matrix = np.array([
        [0, 7, 9, 0, 0, 14],
        [7, 0, 10, 15, 0, 0],
        [9, 10, 0, 11, 0, 2],
        [0, 15, 11, 0, 6, 0],
        [0, 0, 0, 6, 0, 9],
        [14, 0, 2, 0, 9, 0],
    ])
    d_nodes = {'A': [('B',)], 'B': [('A', 3), ('C', 4, True, 'from B to C')], 'C': [('A',)], 'D': [('A', 4)]}
    g = Graph.from_vertices_matrix(v_matrix)
    g2 = DirectedGraph.from_dict(d_nodes)

    node_a = Node('A')
    node_b = Node('B')
    node_c = Node('C')
    node_d = Node('D')
    node_e = Node('E')
    node_f = Node('F')
    node_g = Node('G')

    edge_ad = Edge(node_a, node_d, weight=5, directed=False)
    edge_ab = Edge(node_a, node_b, weight=7, directed=False)
    edge_db = Edge(node_d, node_b, weight=9, directed=False)
    edge_bc = Edge(node_b, node_c, weight=8, directed=False)
    edge_be = Edge(node_b, node_e, weight=7, directed=False)
    edge_ce = Edge(node_c, node_e, weight=5, directed=False)
    edge_de = Edge(node_d, node_e, weight=15, directed=False)
    edge_df = Edge(node_d, node_f, weight=6, directed=False)
    edge_ef = Edge(node_e, node_f, weight=8, directed=False)
    edge_fg = Edge(node_f, node_g, weight=11, directed=False)
    edge_ge = Edge(node_g, node_e, weight=9, directed=False)

    nodes = [node_a, node_b, node_c, node_d, node_e, node_g, node_f]
    nodes2 = deepcopy(nodes)
    edges = [edge_ad, edge_ab, edge_db, edge_bc, edge_be, edge_ce, edge_de, edge_df, edge_ef, edge_fg, edge_ge]

    g3 = Graph(nodes, edges)
    g4 = Graph(nodes2)
    vvd = Visualizer(g3)
    vvd.visualize()
    k = Kruskal(g3)
    grgrgrg = k.tree()
    fvfvfv = Visualizer(grgrgrg)
    fvfvfv.visualize()

    d_gk = {
        '1': [('2', 13), ('3', 18), ('4', 17), ('5', 14), ('6', 22)],
        '5': [('2', 22)],
        '2': [('3', 26)],
        '3': [('4', 3)],
        '4': [('6', 19)],
        '6': []
    }
    g_k = Graph.from_dict(d_gk)
    vk = Visualizer(g_k)
    vk.visualize()
    k = Kruskal(g_k)
    g_tree = k.tree()
    v_tree = Visualizer(g_tree)
    v_tree.visualize()
    print(g.vertices_matrix)
    print(g2.nodes)
    print(g2.edges)
    v = Visualizer(g2)
    v2 = Visualizer(g)
    v3 = Visualizer(g4)
    s = DepthSearch(g2)
    s2 = BreadthFirstSearch(g2)
    print(s.search(g2.nodes[0], g2.nodes[2]))
    print(s2.search(g2.nodes[0], g2.nodes[2]))
    s = DijkstraSearch(g, g.nodes[0])
    print(s.search(g.nodes[3]))
    print(s.search(g.nodes[1]))
    v.visualize()
    v2.visualize()
    v3.visualize()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
