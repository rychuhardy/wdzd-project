import networkx as nx
import numpy as np
import json
import time
import sendgrid
import os
import datetime


def write_time():
    log_file.write("{0}\t".format(datetime.datetime.now()))


graph_path = './data/dataset3/deezer_clean_data/HR_edges.csv'
# graph_path = './data/testdata.txt'
log_file = open("log.txt", 'a', 10)
start_time = time.perf_counter()
graph = nx.read_edgelist(graph_path, delimiter=' ')

write_time()
log_file.write("Loaded graph with {0} nodes and {1} edges\n".format(graph.number_of_nodes(), graph.number_of_edges()))
log_file.flush()

graph_diameter = nx.diameter(graph)

after_diameter_time = time.perf_counter()
write_time()
log_file.write("Finished calculating diameter. Time elapsed: {}s\n".format(after_diameter_time - start_time))
log_file.flush()

values = [0] * graph_diameter
result = {key: list(values) for key in graph.nodes()}

# Calculate graph's k-distances
idx = 0
for node in graph:
    # Logging
    write_time()
    log_file.write("Node {0} out of {1}. Time elapsed {2}s\n".format(idx + 1, graph.number_of_nodes(),
                                                                     time.perf_counter() - start_time))
    log_file.flush()
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
write_time()
log_file.write("Finished algorithm. Time elapsed {}s. Starting writitng result to json.\n".format(
    time.perf_counter() - start_time))

# Save result
json_result = json.dumps(result)

with open("result.json", "w") as output_file:
    output_file.write(json_result)

write_time()
log_file.write("Done.\n")

os.environ['SENDGRID_API_KEY'] = "apikey"

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
data = {
    "personalizations": [
        {
            "to": [
                {
                    "email": "receiver"
                }
            ],
            "subject": "Finished calculating fingerprint"
        }
    ],
    "from": {
        "email": "python@azure.com"
    },
    "content": [
        {
            "type": "text/plain",
            "value": "It's done"
        }
    ]
}
response = sg.client.mail.send.post(request_body=data)

# log_file.write(response.body)
# log_file.write(response.headers)

log_file.close()
