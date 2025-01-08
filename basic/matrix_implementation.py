from basic.data_extraction import *
import numpy as np

recommendations= sp.recommendations(seed_genres=['pop'], limit=100)
album_ids = get_album_id([recommendations])
create_file(album_ids=album_ids, file_name1='pairs2.txt', file_name2='all2.txt')

dic_albums = {}
list_of_albums = []

dic_pairs = {}
list_of_edges = []

def create_matrix():
    with open('all2.txt', 'r') as f:    
        for idx, line in enumerate(f):
            line = line.strip()  
            list_of_albums.append(line)  
            dic_albums[line] = idx

    num_w = len(list_of_albums)
    adjacency_matrix = np.zeros((num_w, num_w), dtype=object) 


    with open('pairs2.txt', 'r') as f:
        line_count = sum(1 for line in f)

    num_e = line_count
    incidence_matrix = np.zeros((num_w, num_e), dtype=object) 

    with open('pairs2.txt', 'r') as f2:
        for idx, line in enumerate(f2):
            line = line.strip()
            w1, w2 = line.split(sep=';')
            w1 = w1.strip()  
            w2 = w2.strip()
            dic_pairs[(w1,w2)] = idx
            list_of_edges.append((w1,w2))

            idx1 = dic_albums.get(w1)
            idx2 = dic_albums.get(w2)

            adjacency_matrix[idx1][idx2] = 1

            incidence_matrix[idx1][idx] = 1
            incidence_matrix[idx2][idx] = 1

    return adjacency_matrix, incidence_matrix


adjacency_matrix, incidence_matrix = create_matrix()
