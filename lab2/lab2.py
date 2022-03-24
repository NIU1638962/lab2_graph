# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 08:25:11 2022

@author: Joel Tapia Salvador
"""
import networkx

def monitor_interest(G):
    # Iterate over every edge in the graph
    for edge in G.edges:
        node1 = edge[0]
        node2 = edge[1]
        G[node1][node2]['weight'] = 0
        assert (0 <= len(G[node1]["topInterests"]) <= 5) and (0 <= len(G[node2]["topInterests"]) <= 5), ("At least one of the nodes of the edge has a not valid number of 'topInterest' elements." + str(G[node1]["topInterests"]) + str(G[node2]["topInterests"]))
        # In every edge we look if an interest of one of the node is in the interests of the other node of the edge: 
        for interest in  G[node1]["topInterests"]:
            if interest in G[node2]["topInterests"]:
                # If the interest is in the secind node we augment the weight of the edge by one:
                G[node1][node2]['weight'] += 1
        assert 0 <= len(G[node1][node2]['weight']) <= 5, ("Weight of the edge is not in the expected range." + str(len(G[node1][node2]['weight'])))
        #  If after procesing the common interest of both nodes the weight remains 0, we can delete the edge. Saves time because we know that the edge will not increase its weight in te future (an edge only have two nodes), and we do not have to iterate over every edge another time to checks its weight and delete it.
        if len(G[node1][node2]['weight']) == 0:
            G.remove_edge(node1, node2)
    return G
