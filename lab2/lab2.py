# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 08:25:11 2022

@author: Joel Tapia Salvador
"""
import networkx


#  Generalization to make easy to edit the code if it is changed the maximum
# possible number of "topInterests".
MAX_POSIBLE_TOPINTERESTS = 5


def monitor_interest(graph):
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
        ) and (0 <= len(graph.nodes[node2]["topInterests"]) <= MAX_POSIBLE_TOPINTERESTS), (
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
