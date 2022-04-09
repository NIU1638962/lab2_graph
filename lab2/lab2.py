# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 08:25:11 2022

@author: Joel Tapia Salvador, Thijs Rood
"""
import networkx
import random
import matplotlib.pyplot as plt
from numpy import number
import pandas as pd
import itertools


#  Generalization to make easy to edit the code if it is changed the maximum
# possible number of "topInterests".
MAX_POSIBLE_TOPINTERESTS = 5


def monitor_interests(graph):
    """
    Given a networkx graph where every node has a property "topInterest" (list
    of element between 0 and 5), and weights ever edge depending on the number
    of common "topIntersts" of both adjecents nodes. If two adjacent nodes
    doesn't any common "topInterests" (weight = 0) the edge is removed.

    Parameters
    ----------
    graph : networkx graph type
        Networkx graph where the nodes have the property "topIntersts".

    Returns
    -------
    grph : networkx graph type
        Networkx graph where the nodes have the property "topIntersts", where
        every edge has a weight between 1 and 5 depending in the common
        "topInterests" of both adjecent nodes.

    """
    # Iterate over every edge in the graph.
    for edge in graph.edges:
        node1 = edge[0]
        node2 = edge[1]
        graph[node1][node2]["weight"] = 0
        assert (
            0 <= len(graph.nodes[node1]["topInterests"]) <= MAX_POSIBLE_TOPINTERESTS
        ) and (
            0 <= len(graph.nodes[node2]["topInterests"]) <= MAX_POSIBLE_TOPINTERESTS
        ), (
            "At least one of the nodes of the edge has a not valid number of "
            + "'topInterest' elements."
            + str(graph.nodes[node1]["topInterests"])
            + str(graph.nodes[node2]["topInterests"])
        )
        # In every edge we look if an interest of one of the node is in the
        # interests of the other node of the edge.
        for interest in graph.nodes[node1]["topInterests"]:
            if interest in graph.nodes[node2]["topInterests"]:
                # If the interest is in the second node we augment the weight
                # of the edge by one.
                graph[node1][node2]["weight"] += 1
        assert 0 <= graph[node1][node2]["weight"] <= MAX_POSIBLE_TOPINTERESTS, (
            "Weight of the edge is not in the expected range."
            + str(graph[node1][node2]["weight"])
        )
        #  If after procesing the common interest of both nodes the weight
        # remains 0, we can delete the edge. Saves time because we know that
        # the edge will not increase its weight in te future (an edge only have
        # two nodes), and we do not have to iterate over every edge another
        # time to checks its weight and delete it.
        if graph[node1][node2]["weight"] == 0:
            graph.remove_edge(node1, node2)
    return graph


"""
We have n dice with k sides with k being platonic.
Order is not neccecary so there are k^n possibilities.
"""
def luckydraw_table(n):

    # some platonic solids have either 4, 6, 8, 12 or 20 faces
    assert (k in [4, 6, 8, 12, 20])

    # set total to 0
    table = [] 

    # rows in the table should range from n to n+9
    for k in [4, 6, 8, 12, 20]:
        krow = []
        for i in range(n, n+9):
            #row = []
            total = 0
            for _ in range(i):
                total = k**i
                #row.append(total)
            krow.append(total)
            
        table.append(krow)
    df = pd.DataFrame(table, index=[k for k in [4, 6, 8, 12, 20]], columns=[str(i) for i in range(n, n+9)])

    print(df)
    return df



def luckydraw_simulation(n, k, v):

    # some platonic solids have either 4, 6, 8, 12 or 20 faces
    assert (k in [4, 6, 8, 12, 20])
    
    # set the number of winners to 0
    number_of_winners = 0

    # loop for 1000 simulations
    for _ in range(1000):
        
        # reset the total value
        total = 0

        # loop over the amount of throws
        for _ in range(n):
            number = random.randint(1, k)
            total += number
        
        # check if we have a winner
        if total > v:
            number_of_winners += 1

    return number_of_winners

# testing
print(luckydraw_simulation(5, 6, 28))


def remove_subdivisions(graph: networkx.Graph):
    
    # loop over nodes
    for node in list(graph.nodes):

        if len(graph.adj[node]) == 2:
            nodelist = list(graph.adj[node])
            print('added edge: ' + str(nodelist[0]) + ' ' + str(nodelist[1]))
            graph.add_edge(nodelist[0], nodelist[1])
            print('removed node ' + str(node))
            graph.remove_node(node)



    return graph

def contains_K5(graph: networkx.Graph):

    k5 = networkx.complete_graph(5)

    nodes = graph.nodes
    for subgraph in (itertools.combinations(nodes, 5)):
        H = graph.subgraph(list(subgraph))
        if networkx.is_isomorphic(k5, H):
            return True
    return False


def contains_K33(graph: networkx.Graph):

    k33 = networkx.complete_bipartite_graph(3,3)
    nodes = graph.nodes
    for subgraph in (itertools.combinations(nodes, 6)):
        H = graph.subgraph(list(subgraph))
        if networkx.is_isomorphic(k33, H):
            return True
    return False

# # quick testing
G = networkx.Graph()
G.add_nodes_from([1, 2, 3, 4])
G.add_edges_from([(1,2),(1,3),(1,4),(3,4)])
contains_K5(G)
# # #print(remove_subdivisions(G))

print("Should return True:")
print(contains_K33(networkx.complete_bipartite_graph(3,3)))
print("Should return True:")
print(contains_K5(networkx.complete_graph(5)))
print("Should return False:")
print(contains_K33(networkx.petersen_graph()))
print("Should return False")
print(contains_K33(networkx.complete_graph(10)))