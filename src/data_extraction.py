from itertools import combinations
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

# łączenie się z API 
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(client_id=client_id,
                                                      client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# zbieranie unikalnych albumów
def get_album_id(list_of_rec):
    album_ids = set()
    for rec in list_of_rec:
        album_ids.update({track['album']['id'] for track in rec['tracks']})
    return album_ids

def artists_from_album(album_id, artist_album_dict):
    album_info = sp.album(album_id)

    tracks = sp.album_tracks(album_id)
    
    for track in tracks['items']:
        for artist in track['artists']:
            artist_name = artist['name']
            if artist_name not in artist_album_dict:
                artist_album_dict[artist_name] = set() 
            artist_album_dict[artist_name].add(album_info['name'])


def create_file(album_ids, file_name1, file_name2):
    artist_album_dict = {}
    for album_id in album_ids:
        artists_from_album(album_id=album_id, artist_album_dict=artist_album_dict)

    album_pairs = set()
    for artist, albums in artist_album_dict.items():
        if len(albums) > 1:
            pairs = combinations(albums, 2)
            album_pairs.update(pairs)

    with open(file_name1, 'w', encoding='utf-8') as f:
        for album1, album2 in album_pairs:
            f.write(f"{album1}; {album2}\n")

    with open(file_name2, 'w', encoding='utf-8') as f:
        for id in album_ids:
            f.write(f"{sp.album(album_id=id)['name']}\n")

def create_file_for_bipartite_graph(album_ids, file_artist, file_albums, file_pais):
    artist_album_dict = {}
    for album_id in album_ids:
        artists_from_album(album_id=album_id, artist_album_dict=artist_album_dict)
    artist_set = set()
    albums_set = set()
    pairs_set = set()
        
    for i in artist_album_dict.items():
        for album in i[1]:
            artist_set.add(i[0])
            albums_set.add(album)
            pairs_set.add(i[0] + '; ' + album)

    with open(file_artist, 'w', encoding='utf-8') as f:
        for a in artist_set:
            f.write(f'{a}\n')
        
    with open(file_albums, 'w', encoding='utf-8') as f:
        for a in albums_set:
            f.write(f'{a}\n')

    with open(file_pais, 'w', encoding='utf-8') as f:
        for a in pairs_set:
            f.write(f'{a}\n')        
        
        

if __name__ == '__main__':
    # pobieranie piosenek 
    recommendations1= sp.recommendations(seed_genres=['pop'], limit=100)
    #recommendations2 = sp.recommendations(seed_genres=['hip-hop'], limit=100)
    #recommendations3 = sp.recommendations(seed_genres=['rock'], limit=100)
    list_of_rec = [recommendations1]
    album_ids = get_album_id(list_of_rec=list_of_rec)
    create_file_for_bipartite_graph(album_ids, 'dane/dane_dwudzielny/artists.txt', 'dane/dane_dwudzielny/albums.txt', 'dane/dane_dwudzielny/pairs.txt' )
    #create_file(album_ids=album_ids, file_name1='albums_pairs3.txt', file_name2='all_albums3.txt')