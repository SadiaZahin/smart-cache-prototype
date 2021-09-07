import random
from src.utils import write_to_json_file

graph = {}


def dfs(u, target):
    if u == target:
        return True
    if u not in graph:
        return False

    for v in graph[u]:
        reach = dfs(v, target)
        if reach:
            return True
    return False


def form_cycle(u, v):
    if u == v:
        return True
    if dfs(u, v):
        return True
    if dfs(v, u):
        return True
    return False


def generate_dag(total_nodes, dependency_count):
    for node in range(1, total_nodes+1):
        graph[node] = []

    total_edges = 0

    for i in range(1, total_nodes*total_nodes):
        u = random.randint(1, total_nodes)
        v = random.randint(1, total_nodes)
        if not form_cycle(u, v):
            total_edges += 1
            graph[u].append(v)

        if total_edges == dependency_count:
            break

    dag_output = {
        "total_servers": total_nodes,
        "servers": [],
    }

    for node in range(1, total_nodes+1):
        min_time = random.randint(0, 1)
        max_time = random.randint(min_time+1, min_time+2)
        server = {
            "server_name": node,
            "dependencies": graph[node],
            "min_time": min_time,
            "max_time": max_time,
        }
        dag_output["servers"].append(server)

    write_to_json_file(dag_output, "./dataset/dag.json")


if __name__ == "__main__":
    generate_dag(20, 25)  # generate_dag(total nodes, dependency count)
