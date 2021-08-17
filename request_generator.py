import random
from src.utils import write_to_json_file


def generate_requests(total_servers, total_requests):
    output = {
        "request_endpoints": []
    }
    for i in range(1, total_requests+1):
        endpoint = random.randint(1, total_servers)
        output["request_endpoints"].append(endpoint)

    write_to_json_file(output, "./dataset/requests.json")


if __name__ == "__main__":
    generate_requests(20, 100)
