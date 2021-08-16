from src.server import Server
import random
import time


class EndPoint():
    def __init__(self, server_name, min_request_time, max_request_time, dependency_objects):
        self.server: Server = Server(server_name, self.get)
        self.min_request_time = min_request_time
        self.max_request_time = max_request_time
        self.dependency_objects = dependency_objects

    def get(self):
        print(f"Called end point: {self.server.server_name}")

        rand_access = random.randint(1, 100)

        if rand_access <= self.server.cache_hit_percentage: # cache hit
            print(f"Cache hit for: {self.server.server_name}")
            return
        
        # cache miss
        rand_request_time = random.uniform(self.min_request_time, self.max_request_time)
        time.sleep(rand_request_time)

        for obj in self.dependency_objects:
            obj.get()
