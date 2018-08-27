import datetime
import json
import os
import time

import networkx as nx
import sendgrid


def compute(input_file, output):
    start_time = time.perf_counter()
    graph = nx.read_edgelist(input_file, delimiter=' ')

    graph_diameter = nx.diameter(graph)

    after_diameter_time = time.perf_counter()

    values = [0] * graph_diameter
    result = {key: list(values) for key in graph.nodes()}

    # Calculate graph's k-distances
    idx = 0
    for node in graph:
        # Logging
        idx = idx + 1

        # Calculate k-distances from node
        successors = list(nx.bfs_successors(graph, source=node))
        distances = dict.fromkeys(graph.nodes(), None)  # distances from source
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

    # print(result)

    # Save result
    json_result = json.dumps(result)

    with open(output, "w") as output_file:
        output_file.write(json_result)


compute("./datasets/all_to_all.txt", "./datasets/results/all_to_all.json")
compute("./datasets/circle.txt", "./datasets/results/circle.json")
compute("./datasets/line.txt", "./datasets/results/line.json")
compute("./datasets/star.txt", "./datasets/results/star.json")
compute("./datasets/two_circles_with_bridge.txt", "./datasets/results/two_circles_with_bridge.json")
