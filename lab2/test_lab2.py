# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 08:30:18 2022

@author: Joel Tapia Salvador
"""
import networkx as nx
import random
import lab2 as lb

SEEDS = ("128856274", "2789578903", "383948939")
N_NODES = ("5", "10", "500")
N_EDGES = ("3", "5", "63000")
N_EDGES_MONITOR = ("1", "2", "62375")

TESTING = 'Testing "{}" function: '
PSD = "\tPassed => "
DELIMITER = "--------------------------------------------------------------"


def create_graph(seed: str, n_nodes: int, n_edges: int, n_edges_monitor: int):
    assert (n_edges <= (((n_nodes ** 2) - n_nodes) / 2)) and (
        n_edges_monitor <= n_edges
    ), "Arguments given don't allow the creation of a graph."
    random.seed(seed)
    graph = nx.Graph()
    node_list = [
        (
            str(i),
            {
                "topInterests": [
                    str(4 * i + j) for j in range(4) if random.randint(0, 9) > 3
                ]
            },
        )
        for i in range(n_nodes)
    ]
    graph.add_nodes_from(node_list)
    edges_list = []
    while len(edges_list) < n_edges:
        t = (str(random.randint(0, n_nodes - 1)), str(random.randint(0, n_nodes - 1)))
        if t not in edges_list and (t[1], t[0]) not in edges_list and t[0] != t[1]:
            edges_list.append(t)
    graph.add_edges_from(edges_list)
    monitor_list = [chr(i) for i in range(n_edges_monitor)]
    for interest, edge in zip(monitor_list, graph.edges):
        times = random.randint(1, 2)
        for i in range(times):
            graph.nodes[edge[0]]["topInterests"].append(interest)
            if (times + 2) < len(graph.nodes[edge[0]]["topInterests"]):
                try:
                    graph.nodes[edge[0]]["topInterests"].pop(0)
                except IndexError:
                    pass
            graph.nodes[edge[1]]["topInterests"].append(interest)
            if (times + 2) < len(graph.nodes[edge[1]]["topInterests"]):
                try:
                    graph.nodes[edge[1]]["topInterests"].pop(0)
                except IndexError:
                    pass
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
        + "\n\t\tObtained numbes of edges => {1}"
        + "\n\t\tExpected number of nodes => {2}"
        + "\n\t\tExpected numbes of edges => {3}"
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
result = []

print(DELIMITER)
try:
    for seed, n_nodes, n_edges, n_edges_monitor in zip(
        SEEDS, N_NODES, N_EDGES, N_EDGES_MONITOR
    ):
        tests = []
        try:
            print("TESTING SEED: " + seed)
            graph = create_graph(seed, int(n_nodes), int(n_edges), int(n_edges_monitor))
            tests.append(graph.copy())
            # Test 1.
            print(TESTING.format("build_monitor_interests()"))
            print(PSD)
            pas, graph = test_monitor_interests(
                graph, int(n_nodes), int(n_edges_monitor)
            )
            print("\t\t" + str(pas))
            TESTS_PASSED += 1
            tests.append(graph.copy())
            # Test 2.

            # Test 3.

            # Test 4.

            GRAPHS_COMPLETED += 1
        except AssertionError as msg:
            print("\t\tFalse: " + str(msg))
        finally:
            result.append(tests)
            print(DELIMITER)
finally:
    print("Graphs completed: " + str(GRAPHS_COMPLETED) + "/" + str(len(SEEDS)))
    print("Tests passed: " + str(TESTS_PASSED) + "/" + str(4 * len(SEEDS)))
