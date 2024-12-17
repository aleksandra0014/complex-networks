import networkx as nx 

class Graph:
    def __init__(self):
        self.graph = nx.Graph()  

    def add_w(self, w):
        self.graph.add_node(w)

    def add_k(self, w1, w2):
        self.graph.add_edge(w1, w2)

    def show_graph(self):
        for wierzcholek in self.graph.nodes:
            neighbors = list(self.graph.neighbors(wierzcholek))
            print(f'{wierzcholek}: {neighbors}')

    def addw_from_file(self, file):
        with open(file, 'r') as f:
            for line in f:
                line = line.strip()
                self.add_w(line)

    def addk_from_file(self, file, bi=False):
        with open(file, 'r') as f:
            for line in f:
                line = line.strip()  
                w1, w2 = line.split(sep=';')  
                w1 = w1.strip()
                w2 = w2.strip()
                
                if bi and w1 == w2:  # Jeśli `bi` jest prawdą i w1 == w2, przejdź do następnej iteracji
                    continue
                
                self.add_k(w1, w2)  

    def shortest_path(self, start, end):
        try:
            path = nx.shortest_path(self.graph, source=start, target=end)
            return path
        except nx.NetworkXNoPath:
            return f'Brak ścieżki między tymi wierzchołkami'
        except nx.NodeNotFound:
            return f'Jeden z wpisanych wierzchołków nie istnieje'
    
    def create_subgraph(self, node):
        if node in self.graph:
            neighbours = list(self.graph.neighbors(node))
            nodes = [node] + neighbours
            subgraph = self.graph.subgraph(nodes)
            return subgraph
        else:
            print('Nie istnieje taki wierzchołek w grafie')
            return None
        
    def neighbours(self, node):
        print(list(self.graph.neighbors(node)))

    def degree2(self):
        return int(self.graph.number_of_nodes())

    def size(self):
        return self.graph.number_of_edges()
    
    def density(self):
        return 2 * self.size() / (self.degree2() * (self.degree2() - 1))
    
    def avg_and_diameter(self): # Średnica = długość najdłuższej z najkrótszych ścieżek
        # Średnia długość ścieżki (z najkrótszych ścieżek dla wszystkich par )
        connected_components = list(nx.connected_components(self.graph))
        
        total_path_sum = 0
        total_pairs = 0
        len_of_the_longest = 0
        
        for component in connected_components:
            subgraph = self.graph.subgraph(component)  
            path_sum = 0
            pairs = 0
            
            for source in subgraph:
                lengths = nx.single_source_shortest_path_length(subgraph, source)
                for i in lengths.values():
                    if i > len_of_the_longest:
                        len_of_the_longest = i
                path_sum += sum(lengths.values())
                pairs += len(lengths) - 1  
                
            total_path_sum += path_sum
            total_pairs += pairs

        if total_pairs > 0:
            return total_path_sum / total_pairs, len_of_the_longest
        else:
            return float('inf')  
    
    def centrality_measures_n(self, node):

        # degree - ile połączonych z nim wierzchołków - dobry hub 
        degree = len(list(self.graph.neighbors(node)))

        # bliskość - odwrotność śreniej odl od innych wierzchołków - oznacza, że wierzchołek szybko osiąga inne wierzchołki, co czyni go efektywnym w przekazywaniu informacji.
        centrality = nx.closeness_centrality(self.graph)[node]

        # pośrednictwo - liczba najkrótszych ścieżek przechodzących przez ten wierzchołek. Może identyfikować "mosty" w grafie, które spajają różne grupy.
        betweenness = nx.betweenness_centrality(self.graph)[node]

        return f'\nStopień: {degree}, \nBliskość: {centrality}, \nPośrednictwo: {betweenness}'
    
    def max_centrality(self):
        d = 0
        c = 0 
        b = 0
        node_d = None
        node_c = None
        node_b = None

        for i in self.graph.nodes:
            if len(list(self.graph.neighbors(i))) > d:
                d = len(list(self.graph.neighbors(i)))
                node_d = i 
            if c < nx.closeness_centrality(self.graph)[i]:
                c = nx.closeness_centrality(self.graph)[i]
                node_c = i
            if b < nx.betweenness_centrality(self.graph)[i]:
                b = nx.betweenness_centrality(self.graph)[i]
                node_b = i
        return f'\nStopień: {d}  node: {node_d}, \nBliskość: {c} node: {node_c}, \nPośrednictwo: {b}  node: {node_b}' 
    
    def centrality_measures_k(self, k):

        # Pośrednictwo = liczba / odsetek najkrótszych DRÓG przechodzących przez krawędź

        edge_betweenness = nx.edge_betweenness_centrality(self.graph)[k]

        return f'\nPośrednictwo: {edge_betweenness}'
    
    def eigenvector_centrality(self, node):

        '''Centralność wektora własnego mierzy wpływ wierzchołka w grafie, biorąc pod uwagę nie tylko 
        liczbę jego sąsiadów, ale także wpływ tych sąsiadów. Węzeł o wysokiej centralności wektora własnego
        jest połączony z innymi węzłami, które również mają dużą centralność.'''
    
        e = nx.eigenvector_centrality(self.graph)[node]

        return f'\nCentralność wektora własnego: {e}'
    
    def page_rank(self, node):

        p = nx.pagerank(self.graph, alpha=0.85)[node]

        return f'\nPagerank: {p}'
    
def iseulerian(g):
    if isinstance(g, Graph):
        g = g.graph  # jesli graf to instacja klasy to trzeba odwołać się do prawidłowego sformułownia graph
    
    if nx.is_eulerian(g): 
        path = list(nx.eulerian_path(g))
        return f'Graf jest eulorowski, a to ścieżka Eulera: {path}'
    else:
        return 'Graf nie jest eulorowski.'

if __name__ == '__main__':
    g = Graph()
    g.addw_from_file(r'C:\Users\aleks\OneDrive\Documents\SIECI_ZLOZONE\dane\all2.txt')
    g.addk_from_file(r'C:\Users\aleks\OneDrive\Documents\SIECI_ZLOZONE\dane\pairs2.txt')
    print('\nWŁASNOŚCI GRAFU')
    print('Stopień:')
    print(g.degree2())
    print('\nRozmiar')
    print(g.size())
    print('\nGęstość')
    print(g.density())
    print('\nŚrednica')
    print(g.avg_and_diameter()[1])
    print('\nŚrednia dł. najkrótszych ścieżek')
    print(g.avg_and_diameter()[0])
    print('---'*20)
    node = input('Podaj nazwe węzła, jeśli nie wiesz jaki to wpisz 0: ')
    if node == '0':
        node = 'Grateful'
    print(f'\nMIARY CENTRALNOŚCI dla węzła {node}')
    print(g.centrality_measures_n(node))
    print(g.eigenvector_centrality(node))
    print(g.page_rank(node))
    print()
    print('MAX')
    print(g.max_centrality())
    print('---'*20)
    k = input('Podaj krawędź, jeśli nie wiesz jaką to wpisz 0: ')
    if k == '0':
        k = ('Hard II Love', 'Grateful')
    print(f'\nMIARY CENTRALNOŚCI dla krawędzi {k}')
    print(g.centrality_measures_k(k))
    
