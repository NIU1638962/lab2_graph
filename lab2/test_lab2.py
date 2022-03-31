# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 08:30:18 2022

@author: Joel Tapia Salvador
"""
import networkx as nx
import random
import lab2 as lb

SEEDS = ("128856274", "2789578903")
N_NODES = ("5", "10")
N_EDGES = ("3", "5")


def create_graph(seed, n_nodes, n_edges):
    random.seed(seed)
    graph = nx.Graph()
    node_list = [(str(i), {"topInterests": []}) for i in range(n_nodes)]
    for node in graph.nodes():
        graph.nodes[node]["topInterests"]
    graph.add_nodes_from(node_list)
    list_edges = []
    while len(list_edges) < n_edges:
        t = (str(random.randint(0, n_nodes - 1)), str(random.randint(0, n_nodes - 1)))
        if t not in list_edges and (t[1], t[0]) not in list_edges and t[0] != t[1]:
            list_edges.append(t)
    graph.add_edges_from(list_edges)

    return graph


result = []
for seed, n_nodes, n_edges in zip(SEEDS, N_NODES, N_EDGES):
    graph = create_graph(seed, int(n_nodes), int(n_edges))
    result.append(lb.monitor_interest(graph))
