import collections

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
        current_latencies.sort()
        if len(current_latencies) == 0:
            return
        tail_idx = int(95 * len(current_latencies) / 100) - 1
        if tail_idx < 0:
            tail_idx = 0
            self.tail_latency = current_latencies[tail_idx]
            print(f"found tail_latency: {self.tail_latency}")
 
    def add_latency(self, latency: int):
        print(f"add_latency for {self.server_name} by {latency}")
        self.latency_list.append(latency)
        self.update_tail_latency()
