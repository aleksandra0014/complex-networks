import streamlit as st
from main import * 

st.header('Graf dotyczący powiązań pomiędzy albumami artystów z platformy Spotify.\n'
          'Dwa albumy są ze sobą połączone, jeśli na obu albumach gra przynjamniej jeden taki sam artysta.')

st.markdown('Najkrótsza ścieżka')


albums = []
with open('all_albums2.txt', 'r') as f:
    for album in f.readlines():
        album = album.strip()
        albums.append(album)



def main_func():
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

main_func()