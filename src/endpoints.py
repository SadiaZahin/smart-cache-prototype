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


def end_point_generator():
    print(f"Called end_point_generator")
    end_point_05 = EndPoint("end_point_05", 0, 1, [])
    end_point_04 = EndPoint("end_point_04", 2, 3, [])

    end_point_03 = EndPoint("end_point_03", 0, 1, [end_point_05])
    end_point_02 = EndPoint("end_point_02", 0, 1, [end_point_04])
    end_point_01 = EndPoint("end_point_01", 1, 2, [end_point_03, end_point_04])
    print(f"Return from end_point_generator")

    return [end_point_01, end_point_02, end_point_03, end_point_04, end_point_05]
