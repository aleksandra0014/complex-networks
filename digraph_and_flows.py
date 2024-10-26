import networkx as nx
import random 

class DGraph:
    def __init__(self):
        self.graph = nx.DiGraph()  

    def add_w(self, w):
        self.graph.add_node(w)

    def add_k(self, w1, w2, capacity=1):  
        self.graph.add_edge(w1, w2, capacity=capacity)

    def show_graph(self):
        for wierzcholek in self.graph.nodes:
            neighbors = list(self.graph.neighbors(wierzcholek))
            print(f'{wierzcholek}: {neighbors}')

    def addw_from_file(self, file):
        with open(file, 'r') as f:
            for line in f:
                line = line.strip()
                self.add_w(line)

    def addk_from_file(self, file):
        with open(file, 'r') as f:
            for line in f:
                line = line.strip()
                w1, w2 = line.split(sep=';')  
                w1 = w1.strip()
                w2 = w2.strip()
                capacity = random.randint(1, 9)
                self.add_k(w1, w2, capacity)

    def shortest_path(self, start, end):
        try:
            path = nx.shortest_path(self.graph, source=start, target=end)
            return path
        except nx.NetworkXNoPath:
            return f'Brak ścieżki między tymi wierzchołkami'
        except nx.NodeNotFound:
            return f'Jeden z wpisanych wierzchołków nie istnieje'

    def max_flow(self, source, sink):
        flow_value, flow_dict = nx.maximum_flow(self.graph, source, sink)
        return (f"Maksymalny przepływ od {source} do {sink} wynosi: {flow_value}")
        
    def neighbours(self, node):
        print(list(self.graph.neighbors(node)))
    
    def show_edges(self):
        print("Krawędzie i ich przepustowości:")
        for u, v, data in self.graph.edges(data=True):
            print(f"Krawędź {u} -> {v}, Przepustowość: {data['capacity']}")


if __name__ == '__main__':
    g = DGraph()
    g.addw_from_file(r'C:\Users\aleks\OneDrive\Documents\SIECI_ZLOZONE\all_albums2.txt')
    g.addk_from_file(r'C:\Users\aleks\OneDrive\Documents\SIECI_ZLOZONE\albums_pairs2.txt')

    source = 'Grateful'  
    sink = 'Slime Season 3'      
    print(g.max_flow(source, sink))
    #g.show_edges()
