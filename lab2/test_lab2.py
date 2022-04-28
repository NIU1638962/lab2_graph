# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 08:30:18 2022

@author: Joel Tapia Salvador
"""
import networkx as nx
import random
import matplotlib.pyplot as plt
import lab2 as lb

SEEDS = (
    "879768679",
    "128856274",
    "2789578903",
    "456789740",
    "700003439",
    "586908490",
    "916168850",
    "904186932",
    "678685870",
    "383948930",
)
N_NODES = ("3", "5", "10", "5", "6", "6", "10", "10", "26", "500")
N_EDGES = ("2", "3", "5", "10", "9", "15", "15", "15", "200", "1250")
N_EDGES_MONITOR = ("2", "1", "2", "10", "9", "15", "15", "15", "65", "1250")
K_5 = (False, False, False, True, False, True, False, False, False, False)
K_3_3 = (False, False, False, False, True, True, False, False, True, True)

TESTING = 'Testing "{}" function: '
PSD = "\tPassed => "
DELIMITER = "--------------------------------------------------------------"


def create_graph(seed: str, n_nodes: int, n_edges: int, n_edges_monitor: int):
    # By deduction, given that every node only can have 5 interests, the
    # maximun amount of edges that the graf can have after the
    # monitor_interest() function is
    assert (n_edges <= (((n_nodes ** 2) - n_nodes) / 2)) and (
        n_edges_monitor <= ((n_nodes // 2) * 5)
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
    # Expected properties of the graph.
    expected_number_of_nodes = n_nodes
    expected_number_of_edges = n_edges_monitor
    # Generates de graph using the function tested.
    graph = lb.monitor_interests(graph)
    # Gets the values of the properties of the test graph using networkx
    # build in methods and functions.
    obtained_number_of_nodes = graph.number_of_nodes()
    obtained_number_of_edges = graph.number_of_edges()
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


def test_remove_subdivisions(graph):
    # Expected properties of the graph.
    remove_node = len([1 for node in graph.nodes() if nx.degree(graph, node) == 2])
    expected_number_of_nodes = graph.number_of_nodes() - remove_node
    expected_number_of_edges = graph.number_of_edges() - remove_node
    # Generates de graph using the function tested.
    graph = lb.remove_subdivisions(graph)
    # Gets the values of the properties of the test graph using networkx
    # build in methods and functions.
    obtained_number_of_nodes = graph.number_of_nodes()
    obtained_number_of_edges = graph.number_of_edges()
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


def test_contains_K5(graph, expected_result):
    # Generates de graph using the function tested.
    obtained_result = lb.contains_K5(graph)
    t = "\n\t\tObtained result => {0}" + "\n\t\tExpected result => {1}"
    t = t.format(obtained_result, expected_result,)
    assert obtained_result == expected_result, (
        "Returned value doesn't match with expected result." + t
    )
    return True


def test_contains_K33(graph, expected_result):
    # Generates de graph using the function tested.
    obtained_result = lb.contains_K33(graph)
    t = "\n\t\tObtained result => {0}" + "\n\t\tExpected result => {1}"
    t = t.format(obtained_result, expected_result,)
    assert obtained_result == expected_result, (
        "Returned value doesn't match with expected result." + t
    )
    return True


TESTS_PASSED = 0
GRAPHS_COMPLETED = 0
result = []

print(DELIMITER)
try:
    for seed, n_nodes, n_edges, n_edges_monitor, test_3, test_4 in zip(
        SEEDS, N_NODES, N_EDGES, N_EDGES_MONITOR, K_5, K_3_3
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
            print(TESTING.format("remove_subdivisions()"))
            print(PSD)
            pas, graph = test_remove_subdivisions(graph)
            print("\t\t" + str(pas))
            TESTS_PASSED += 1
            tests.append(graph.copy())

            # Test 3.
            print(TESTING.format("contains_K5()"))
            print(PSD)
            pas = test_contains_K5(graph, test_3)
            print("\t\t" + str(pas))
            TESTS_PASSED += 1

            # Test 4.
            print(TESTING.format("contains_K33()"))
            print(PSD)
            pas = test_contains_K33(graph, test_4)
            print("\t\t" + str(pas))
            TESTS_PASSED += 1

            GRAPHS_COMPLETED += 1
        except AssertionError as msg:
            if len(tests) < 3:
                tests.append(graph.copy())
            print("\t\tFalse: " + str(msg))
        finally:
            result.append(tests)
            for graph in tests:
                nx.draw(graph, with_labels=True, font_weight="bold")
                plt.show()
            print(DELIMITER)
finally:
    print("Graphs completed: " + str(GRAPHS_COMPLETED) + "/" + str(len(SEEDS)))
    print("Tests passed: " + str(TESTS_PASSED) + "/" + str(4 * len(SEEDS)))
    print("Tests passed: " + str(TESTS_PASSED) + "/" + str(4 * len(SEEDS)))
