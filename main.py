import networkx as nx
import numpy as np
import json

#graph_path = './data/dataset2/CA-GrQc.txt'
graph_path = './data/testdata.txt'

graph = nx.read_edgelist(graph_path)

print("Loaded graph with {0} nodes and {1} edges".format(graph.number_of_nodes(), graph.number_of_edges()))

graph_diameter = nx.diameter(graph)

result = dict.fromkeys(graph.nodes(), [None]*graph_diameter)
# result = np.zeros(shape=(graph.number_of_nodes(), graph_diameter))

# Calculate graph's k-distances
idx = 0
for node in graph:
    # Logging
    print("Node {0} out of {1}".format(idx, graph.number_of_nodes()))
    idx = idx + 1

    # Calculate k-distances from node
    successors = list(nx.bfs_successors(graph, source = node))
    for k in range(0, len(successors)): # This doesn't work - refactor
        result[node][k] = len(successors[k][1])


print(result)

# Save result
json_result = json.dumps(result)

with open("result.json", "w") as output_file:
    output_file.write(json_result)
