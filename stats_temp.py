from src.utils import read_from_json_file, write_to_json_file


server_latencies_only_robinhood = read_from_json_file('./dataset/server_latencies_only_robinhood.json')
server_latencies_clustered = read_from_json_file('./dataset/server_latencies.json')


std_robinhood = []

temp1 = server_latencies_only_robinhood['server_tail_latencies']


for i in range(1,21):
    server_name = 'end_point_' + str(i)
    for j in range(0,20):
        if temp1[j]['server_name'] == server_name:
            print(temp1[j]['server_name'], temp1[j]['tail_latency'])
            std_robinhood.append(float("{:.2f}".format(float(temp1[j]['tail_latency']))))
            break




clustered_robinhood = []

temp1 = server_latencies_clustered['server_tail_latencies']


for i in range(1,21):
    server_name = 'end_point_' + str(i)
    for j in range(0,20):
        if temp1[j]['server_name'] == server_name:
            print(temp1[j]['server_name'], temp1[j]['tail_latency'])
            clustered_robinhood.append(float("{:.2f}".format(float(temp1[j]['tail_latency']))))
            break


print(std_robinhood)

print(clustered_robinhood)