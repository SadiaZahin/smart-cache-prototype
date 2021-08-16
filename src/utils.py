import json


def find_tail_latency(latency_list):
    latency_list.sort()
    if len(latency_list) == 0:
        return 0
    tail_idx = int(99 * len(latency_list) / 100) - 1
    if tail_idx < 0:
        tail_idx = 0
    return latency_list[tail_idx]


def read_from_json_file(file_name):
    with open(file_name, 'r') as myfile:
        data = myfile.read()
        return json.loads(data)


def write_to_json_file(data, file_name):
    with open(file_name, "w") as myfile:
        json.dump(data, myfile, indent=4, sort_keys=True)