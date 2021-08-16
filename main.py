from src.endpoints import EndPoint
from typing import List
import random
import time
from src.utils import read_from_json_file, find_tail_latency
from src.topological_sort import TopologicalGraph
from src.cluster import Cluster


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
            clusters.append(cluster)
            cluster_id += 1

    if single_cluster:
        cluster = Cluster(f"cluster_{cluster_id}", all_end_point_list)
        clusters.append(cluster)

    return clusters


def main(single_cluster=False):
    print(f"Initialize main worker")
    clusters: List[Cluster] = cluster_generator(single_cluster)

    for cluster in clusters:
        cluster.print_cluster()

    print(f"\n\nSTART PROCESSING REQUESTS:\n\n")

    for i in range(1, 11):
        print(f"REQUEST NUMBER: {i}")
        rand_cluster_idx = random.randint(0, len(clusters)-1)
        cluster = clusters[rand_cluster_idx]

        rand_endpoint_idx = random.randint(0, len(cluster.end_points_list)-1)
        end_point = cluster.end_points_list[rand_endpoint_idx]

        st_time = time.time()
        print(f"Initiate API call to cluster: {cluster.cluster_name} -> end point: {end_point.server.server_name}")
        end_point.get()
        ed_time = time.time()
        response_time = ed_time - st_time
        print(f"Finished API call to end point: {end_point.server.server_name}, time taken: {response_time}")

        cluster.robinhood.add_server_latency(end_point.server.server_name, response_time)
        print(f"\n\n")

    all_latencies = []

    for cluster in clusters:
        cluster.print_latency()
        for endpoint in cluster.end_points_list:
            all_latencies.extend(endpoint.server.latency_list)

    overall_system_tail_latency = find_tail_latency(all_latencies)
    print(f"Overall System Tail Latency: {overall_system_tail_latency}")

    print(f"\n\nEND PROCESSING REQUESTS:\n\n")


if __name__ == "__main__":
    main(single_cluster=False)
