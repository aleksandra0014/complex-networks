import networkx as nx 

class Graph:
    def __init__(self):
        self.graph = nx.Graph()  

    def add_w(self, w):
        self.graph.add_node(w)

    def add_k(self, w1, w2):
        self.graph.add_edge(w1, w2)

    def pokaz_graf(self):
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
                self.add_k(w1, w2)

    def shortest_path(self, start, end):
        try:
            path = nx.shortest_path(self.graph, source=start, target=end)
            return path
        except nx.NetworkXNoPath:
            return f'Brak ścieżki między tymi wierzchołkami'
        except nx.NodeNotFound:
            return f'Jeden z wpisanych wierzchołków nie istnieje'
    
if __name__ == '__main__':
    g = Graph()
    g.addw_from_file(r'C:\Users\aleks\OneDrive\Documents\SIECI_ZLOZONE\all_albums2.txt')
    g.addk_from_file(r'C:\Users\aleks\OneDrive\Documents\SIECI_ZLOZONE\albums_pairs2.txt')
    print(g.shortest_path('Sweetener' ,'Grateful')) 