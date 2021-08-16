def find_tail_latency(latency_list):
    latency_list.sort()
    if len(latency_list) == 0:
        return 0
    tail_idx = int(99 * len(latency_list) / 100) - 1
    if tail_idx < 0:
        tail_idx = 0
    return latency_list[tail_idx]