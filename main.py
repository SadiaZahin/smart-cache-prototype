from src.endpoints import EndPoint
from typing import List
import random
import time
from src.utils import read_from_json_file, find_tail_latency, write_to_json_file
from src.topological_sort import TopologicalGraph
from src.cluster import Cluster
import csv
from itertools import zip_longest


def cluster_generator(single_cluster=False):
    print(f"Called end_point_generator")

    graph_raw_data = read_from_json_file("./dataset/dag.json")
    server_data = {}

    total_servers = graph_raw_data["total_servers"]
    topological_graph = TopologicalGraph(total_servers)

    for server in graph_raw_data["servers"]:
        server_name = server["server_name"]
        for dependency_server in server["dependencies"]:
            topological_graph.add_edge(server_name, dependency_server)

        server_data[server_name] = {
            "min_time": server["min_time"],
            "max_time": server["max_time"],
            "dependencies": server["dependencies"],
        }

    print(topological_graph.graph)
    topological_graph.build_clusters()
    print("node_clusters: ", topological_graph.clusters)

    end_point_reference = {}
    cluster_reference = {}
    clusters: List[Cluster] = []

    cluster_id = 1

    all_end_point_list: List[EndPoint] = []

    for cluster in topological_graph.clusters:
        end_point_list: List[EndPoint] = []
        for server_name in cluster:
            dependency_end_points: List[EndPoint] = []
            for node in server_data[server_name]["dependencies"]:
                if node not in end_point_reference:
                    raise Exception("Pre requisite end point not initialized")
                dependency_end_points.append(end_point_reference[node])

            min_time = server_data[server_name]["min_time"]
            max_time = server_data[server_name]["max_time"]
            end_point = EndPoint(f"end_point_{server_name}", min_time, max_time, dependency_end_points)
            end_point_reference[server_name] = end_point
            end_point_list.append(end_point)

        if single_cluster:
            all_end_point_list.extend(end_point_list)
        else:
            cluster = Cluster(f"cluster_{cluster_id}", end_point_list)
            for endpoint in end_point_list:
                cluster_reference[endpoint.server.server_name] = cluster
            clusters.append(cluster)
            cluster_id += 1

    if single_cluster:
        cluster = Cluster(f"cluster_{cluster_id}", all_end_point_list)
        clusters.append(cluster)
        for endpoint in all_end_point_list:
            cluster_reference[endpoint.server.server_name] = cluster

    return clusters, end_point_reference, cluster_reference


def main(single_cluster=False):
    print(f"Initialize main worker")
    clusters, end_point_reference, cluster_reference = cluster_generator(single_cluster)

    print("end_point_reference: ", end_point_reference)
    print("cluster_reference: ", cluster_reference)

    for cluster in clusters:
        cluster.print_cluster()

    print(f"\n\nSTART PROCESSING REQUESTS:\n\n")
    request_data = read_from_json_file("./dataset/requests.json")
    request_list = request_data["request_endpoints"]

    request_no = 1
    for endpoint_id in request_list:
        print(f"REQUEST NUMBER: {request_no}, endpoint_id: {endpoint_id}")
        request_no += 1
        end_point = end_point_reference[endpoint_id]

        st_time = time.time()
        print(f"Initiate API call to end point: {end_point.server.server_name}")
        end_point.get()
        ed_time = time.time()
        response_time = ed_time - st_time
        print(f"Finished API call to end point: {end_point.server.server_name}, time taken: {response_time}")
        cluster = cluster_reference[f"end_point_{endpoint_id}"]
        cluster.robinhood.add_server_latency(end_point.server.server_name, response_time)
        print(f"\n\n")

    list_of_server_names = []
    list_of_server_latencies = []
    all_latencies = []
    for cluster in clusters:
        cluster.print_latency()
        for endpoint in cluster.end_points_list:
            all_latencies.extend(endpoint.server.latency_list)
            list_of_server_latencies.append(list(endpoint.server.latency_list))
            list_of_server_names.append(endpoint.server.server_name)


    overall_system_tail_latency = find_tail_latency(all_latencies)
    print(f"Overall System Tail Latency: {overall_system_tail_latency}")
    all_latencies_data = {
        "all_latencies": all_latencies
    }
    write_to_json_file(all_latencies_data, "./dataset/all_latencies.json")
    #write_to_json_file(all_latencies_data, "./dataset/all_latencies_only_robinhood.json")

    print(f"\n\nEND PROCESSING REQUESTS:\n\n")


if __name__ == "__main__":
    main(single_cluster=False)
