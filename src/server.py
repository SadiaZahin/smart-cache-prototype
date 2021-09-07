import collections
from src.utils import find_tail_latency

"""
    The Server class for endpoints.
    It'll contain the functionalities for maintaining the latencies.
"""


class Server:
 
    def __init__(self, server_name, server_func):
        self.server_name = server_name
        self.server_func = server_func
        self.latency_list = collections.deque()
        self.tail_latency = 0
        self.cache_hit_percentage = 0
 
    def update_tail_latency(self):
        print(f"update_tail_latency for {self.server_name}")
        current_latencies = list(self.latency_list)
        self.tail_latency = find_tail_latency(current_latencies)
        print(f"found tail_latency: {self.tail_latency}")
 
    def add_latency(self, latency: int):
        print(f"add_latency for {self.server_name} by {latency}")
        self.latency_list.append(latency)
        self.update_tail_latency()
