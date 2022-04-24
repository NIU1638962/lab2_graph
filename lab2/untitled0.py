# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 20:57:25 2022

@author: JoelT
"""
import networkx as nx
import random
import matplotlib.pyplot as plt
import lab2 as lb

SEED = "900000000"
# SEEDS = [str(7000000140 + i) for i in range(20)]

# N_NODES = ["6" for i in range(20)]
# N_EDGES = ["9" for i in range(20)]
# N_EDGES_MONITOR = ["9" for i in range(20)]

TESTING = 'Testing "{}" function: '
PSD = "\tPassed => "
DELIMITER = "--------------------------------------------------------------"


def create_graph(seed: str, n_nodes: int, n_edges: int, n_edges_monitor: int):
    assert (n_edges <= (((n_nodes ** 2) - n_nodes) / 2)) and (
        n_edges_monitor <= ((n_nodes // 2) * 5) and (n_edges_monitor <= n_edges_monitor)
    ), "Arguments given don't allow the creation of a graph."
    random.seed(seed)
    graph = nx.Graph()
    node_list = [(str(i), {"topInterests": []}) for i in range(n_nodes)]
    graph.add_nodes_from(node_list)
    i = 0
    while graph.number_of_edges() < n_edges_monitor:
        edge = (
            str(random.randint(0, n_nodes - 1)),
            str(random.randint(0, n_nodes - 1)),
        )
        if (
            len(graph.nodes[edge[0]]["topInterests"]) < 5
            and len(graph.nodes[edge[1]]["topInterests"]) < 5
            and edge not in graph.edges()
            and edge[0] != edge[1]
        ):
            graph.add_edge(edge[0], edge[1])
            graph.nodes[edge[0]]["topInterests"].append(chr(i))
            graph.nodes[edge[1]]["topInterests"].append(chr(i))
            i += 1
    edges = [edge for edge in graph.edges()]
    for j in range((random.randint(1, n_edges_monitor))):
        edge = edges[random.randint(0, len(edges) - 1)]
        if (
            len(graph.nodes[edge[0]]["topInterests"]) < 5
            and len(graph.nodes[edge[1]]["topInterests"]) < 5
        ):
            graph.nodes[edge[0]]["topInterests"].append(chr(i))
            graph.nodes[edge[1]]["topInterests"].append(chr(i))
            i += 1
    while graph.number_of_edges() < n_edges:
        edge = (
            str(random.randint(0, n_nodes - 1)),
            str(random.randint(0, n_nodes - 1)),
        )
        if edge not in graph.edges() and edge[0] != edge[1]:
            graph.add_edge(edge[0], edge[1])
    for node in graph.nodes():
        if len(graph.nodes[node]["topInterests"]) == 0:
            graph.nodes[node]["topInterests"] = [
                str(5 * int(node) + i) for i in range(5) if random.randint(0, 9) > 3
            ]
        elif len(graph.nodes[node]["topInterests"]) < 5 and random.randint(0, 9) > 9:
            graph.nodes[node]["topInterests"].append(
                random.randint((5 * int(node)), (5 * int(node) + 4))
            )
    return graph


def test_monitor_interests(graph: nx.Graph, n_nodes: int, n_edges_monitor: int):
    graph = lb.monitor_interests(graph)
    # Gets the values of the properties of the expected graph using networkx
    # build in methods anf functions.
    expected_number_of_nodes = graph.number_of_nodes()
    expected_number_of_edges = graph.number_of_edges()
    # Generates de graph using the function tested and the test files.
    # Gets the values of the properties of the test graph using networkx
    # build in methods and functions.
    obtained_number_of_nodes = n_nodes
    obtained_number_of_edges = n_edges_monitor
    # Error message in case conditions are not achived.
    t = (
        "\n\t\tObtained number of nodes => {0}"
        + "\n\t\tObtained number of edges => {1}"
        + "\n\t\tExpected number of nodes => {2}"
        + "\n\t\tExpected number of edges => {3}"
    )
    t = t.format(
        obtained_number_of_nodes,
        obtained_number_of_edges,
        expected_number_of_nodes,
        expected_number_of_edges,
    )
    # Verifies number of nodes.
    assert obtained_number_of_nodes == expected_number_of_nodes, (
        "Number of nodes doesn't match with expected result." + t
    )
    # Verifies number of edges.
    assert obtained_number_of_edges == expected_number_of_edges, (
        "Number of edges doesn't match with expected result." + t
    )
    return True, graph


TESTS_PASSED = 0
GRAPHS_COMPLETED = 0
graph = nx.Graph()

petersen = nx.petersen_graph()
print(DELIMITER)
try:
    i = 4230499
    while i < 99999999:
        # and not nx.is_isomorphic(peterson, graph)
        seed = str(int(SEED) + i)
        tests = []
        try:
            # print("TESTING SEED: " + seed)
            graph = create_graph(seed, 10, 15, 15)
            tests.append(graph.copy())
            # Test 1.
            # print(TESTING.format("build_monitor_interests()"))
            # print(PSD)
            pas, graph = test_monitor_interests(graph, 10, 15)
            # print("\t\t" + str(pas))
            TESTS_PASSED += 1
            tests.append(graph.copy())

            #     # Test 2.

            #     # Test 3.

            #     # Test 4.

            GRAPHS_COMPLETED += 1
        except AssertionError:
            tests.append(graph.copy())
            # print("\t\tFalse: " + str(msg))
        finally:
            degrees = [graph.degree(node) for node in graph.nodes()]
            degree = degrees.count(3)
            if degree == 10:
                print("TESTING SEED: " + seed)
                for graph in tests:
                    nx.draw(graph, with_labels=True, font_weight="bold")
                    plt.show()
                print(DELIMITER)
                if nx.is_isomorphic(petersen, tests[1]):
                    break
            i += 1
finally:
    pass
#     print("Graphs completed: " + str(GRAPHS_COMPLETED) + "/" + str(len(SEEDS)))
#     print("Tests passed: " + str(TESTS_PASSED) + "/" + str(4 * len(SEEDS)))
