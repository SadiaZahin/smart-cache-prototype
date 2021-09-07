from src.endpoints import EndPoint
from typing import List
from src.robinhood import RobinHood

"""
    Every Cluster object will contain all the servers and their end points.
    They will also have a Robinhood instance associated with them.
"""


class Cluster:

    def __init__(self, cluster_name: str, end_points_list: List[EndPoint]):
        self.cluster_name = cluster_name
        self.end_points_list = end_points_list
        self.total_end_points = len(end_points_list)
        server_list = [end_point.server for end_point in end_points_list]
        self.robinhood = RobinHood(100, server_list)

    def print_cluster(self):
        print(f"Cluster: {self.cluster_name}[{self.total_end_points}]: ")
        for endpoint in self.end_points_list:
            print(f"{endpoint.server.server_name}")
        print("\n")

    def print_latency(self):
        tail_latency_list = [endpoint.server.tail_latency for endpoint in self.end_points_list]
        overall_tail_latency = self.robinhood.overall_tail_latency
        print(f"Cluster: {self.cluster_name}: tail_latency_list: {tail_latency_list}, overall_tail_latency: {overall_tail_latency}")
