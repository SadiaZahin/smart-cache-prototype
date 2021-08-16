from src.server import Server
from typing import List, Dict
from src.utils import find_tail_latency

class RobinHood:
    def __init__(self, cache_memory_limit: int, server_list: List[Server]):
        self.cache_memory_limit = cache_memory_limit
        self.cache_memory_used = 0
        self.server_list = server_list
        self.server_map: Dict[str, Server] = {}
        self.overall_tail_latency = 0

        avg_cache_hit_ratio = 100/len(server_list)
 
        for server in server_list:
            self.server_map[server.server_name] = server
            server.cache_hit_percentage = avg_cache_hit_ratio
        self.current_cache_allocation()
    
    def add_server_latency(self, server_name, new_latency):
        print(f"add_server_latency for {server_name} with {new_latency}")
        if server_name not in self.server_map:
            raise Exception("Invalid server name provided")
        
        server = self.server_map[server_name]
        server.add_latency(new_latency)
        self.reallocate_cache()
        self.current_tail_latencies()
  
    def reallocate_cache(self):
        print(f"reallocate_cache for robinhood cluster")
        min_latency_server = None
        max_latency_server = None
 
        for server in self.server_list:
            if min_latency_server is None:
                min_latency_server = server
            
            if server.tail_latency < min_latency_server.tail_latency:
                min_latency_server = server

            if max_latency_server is None:
                max_latency_server = server
            
            if server.tail_latency > max_latency_server.tail_latency:
                max_latency_server = server

        allocate_amount = min_latency_server.cache_hit_percentage/2

        max_latency_server.cache_hit_percentage += allocate_amount
        min_latency_server.cache_hit_percentage -= allocate_amount
        self.find_overall_tail_latency()
        self.current_cache_allocation()
    
    def current_cache_allocation(self):
        cache_hit_list = [server.cache_hit_percentage for server in self.server_list]
        print(f"Current cache_hit_list: {cache_hit_list}")
    
    def current_tail_latencies(self):
        tail_latencies = [server.tail_latency for server in self.server_list]
        print(f"Current tail_latencies: {tail_latencies}")

    def find_overall_tail_latency(self):
        latency_list = [server.tail_latency for server in self.server_list]
        self.overall_tail_latency = find_tail_latency(latency_list)
        print(f"Current overall_tail_latency: {self.overall_tail_latency}")
    