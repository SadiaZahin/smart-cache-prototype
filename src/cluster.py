from src.endpoints import EndPoint
from typing import List
from src.robinhood import RobinHood


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
