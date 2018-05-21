import networkx as nx
import numpy as np
import json

graph_path = './data/dataset3/deezer_clean_data/HR_edges.csv'
#graph_path = './data/testdata.txt'

graph = nx.read_edgelist(graph_path, delimiter=',')

print("Loaded graph with {0} nodes and {1} edges".format(graph.number_of_nodes(), graph.number_of_edges()))

graph_diameter = nx.diameter(graph)
values = [0]*graph_diameter
result = {key: list(values) for key in graph.nodes()}

# Calculate graph's k-distances
idx = 0
for node in graph:
    # Logging
    print("Node {0} out of {1}".format(idx+1, graph.number_of_nodes()))
    idx = idx + 1

    # Calculate k-distances from node
    successors = list(nx.bfs_successors(graph, source = node))
    distances = dict.fromkeys(graph.nodes(), None) # distances from source
    for n in range(0, len(successors)):
        if n == 0:
            for x in successors[n][1]:
                distances[x] = 1
        else:
            key = successors[n][0]
            keyDist = distances[key]
            for x in successors[n][1]:
                distances[x] = keyDist + 1

    for n, dist in distances.items():
        if n != node:
            # dist - 1 because indexing starts at 0, so it's easier. It output this means that neighbours have distance equal to zero.
            result[node][dist - 1] = result[node][dist - 1] + 1

print(result)

# Save result
json_result = json.dumps(result)

with open("result.json", "w") as output_file:
    output_file.write(json_result)
