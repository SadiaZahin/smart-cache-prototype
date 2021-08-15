from endpoints import end_point_generator, EndPoint
from typing import List
import random
import time
from robinhood import RobinHood

def main():
    print(f"Initialize main worker")
    end_points: List[EndPoint] = end_point_generator()
    print(f"Generated end_points: {end_points}")

    server_list = [end_point.server for end_point in end_points]
    robinhood = RobinHood(100, server_list)

    print(f"\n\nSTART PROCESSING REQUESTS:\n\n")

    for i in range(1, 1001):
        print(f"REQUEST NUMBER: {i}")
        rand_idx = random.randint(0, len(end_points)-1)
        end_point = end_points[rand_idx]
        st_time = time.time()
        print(f"Initiate API call to end point: {end_point.server.server_name}")
        end_point.get()
        ed_time = time.time()
        response_time = ed_time - st_time
        print(f"Finished API call to end point: {end_point.server.server_name}, time taken: {response_time}")

        robinhood.add_server_latency(end_point.server.server_name, response_time)
        print(f"\n\n")

    print(f"\n\nEND PROCESSING REQUESTS:\n\n")

if __name__ == "__main__":
    main()
