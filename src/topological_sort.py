
class TopologicalGraph:
    def __init__(self, total_nodes):
        self.graph = {}
        self.reverse_graph = {}
        self.total_nodes = total_nodes
        self.dependeny_count = {}
        self.clusters = []

        for node in range(1, total_nodes+1):
            self.graph[node] = []
            self.reverse_graph[node] = []
            self.dependeny_count[node] = 0
    
    def add_edge(self, node_1, node_2):
        self.graph[node_1].append(node_2)
        self.reverse_graph[node_2].append(node_1)
        self.dependeny_count[node_1] += 1

    def build_clusters(self):
        top_layer_nodes = []

        for node in range(1, self.total_nodes+1):
            if self.dependeny_count[node] == 0:
                top_layer_nodes.append(node)

        while len(top_layer_nodes) > 0:
            self.clusters.append(top_layer_nodes)
            next_layer_nodes = []
            for node in top_layer_nodes:
                for dependent_node in self.reverse_graph[node]:
                    self.dependeny_count[dependent_node] -= 1
                    if self.dependeny_count[dependent_node] == 0:
                        next_layer_nodes.append(dependent_node)
            top_layer_nodes = next_layer_nodes
