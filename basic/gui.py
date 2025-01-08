import streamlit as st
from main_Graph import * 
from basic.digraph_and_flows import *

albums = []
with open('all_albums2.txt', 'r') as f:
    for album in f.readlines():
        album = album.strip()
        albums.append(album)


def main_func():
    st.header('Graf dotyczący powiązań pomiędzy albumami artystów z platformy Spotify.\n'
          'Dwa albumy są ze sobą połączone, jeśli na obu albumach gra przynjamniej jeden taki sam artysta.')

    st.subheader('**Najkrótsza ścieżka**')
    g = Graph()
    g.addw_from_file(r'C:\Users\aleks\OneDrive\Documents\SIECI_ZLOZONE\all_albums2.txt')
    g.addk_from_file(r'C:\Users\aleks\OneDrive\Documents\SIECI_ZLOZONE\albums_pairs2.txt')

    choice1 = st.selectbox('Wybierz pierwszy album', albums)
    choice2 = st.selectbox('Wybierz drugi album', albums)

    path = g.shortest_path(choice1, choice2)
    if type(path) == list:
        l = len(path)
    else:
        l = '∞'
    st.text(f'Ścieżka {path}')
    st.text(f'Długość trasy to {l}')

    st.markdown("<br>", unsafe_allow_html=True) 

    st.subheader('Czy graf jest eulerowski?')
    st.text(iseulerian(g))

    st.markdown("<br>", unsafe_allow_html=True) 

    st.subheader('Stwórz podgraf i sprawdź czy jest eulerowski')
    w = st.selectbox('Wybierz wierzchołek (album)', albums)
    subg = g.create_subgraph(w)
    st.text(iseulerian(subg))

    st.markdown("<br>", unsafe_allow_html=True) 

    st.subheader('Maksymalny przepływ między dwoma wierzchołkami.')
    gd = DGraph()
    gd.addw_from_file(r'C:\Users\aleks\OneDrive\Documents\SIECI_ZLOZONE\all_albums2.txt')
    gd.addk_from_file(r'C:\Users\aleks\OneDrive\Documents\SIECI_ZLOZONE\albums_pairs2.txt')
    source = st.selectbox('Wybierz źródło', albums,  index=1) 
    sink = st.selectbox('Wybierz ujście', albums,  index=2)      
    st.text(gd.max_flow(source, sink))

    
main_func()