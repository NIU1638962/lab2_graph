import networkx as nx

a = nx.Graph()
a.add_edge(1, 2)
a[1][2]['weight'] = 0
print(a[1][2]['weight'])