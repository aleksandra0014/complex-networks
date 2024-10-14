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

# pobieranie piosenek 
recommendations1= sp.recommendations(seed_genres=['pop'], limit=100)
recommendations2 = sp.recommendations(seed_genres=['hip-hop'], limit=100)
recommendations3 = sp.recommendations(seed_genres=['rock'], limit=100)


# zbieranie unikalnych albumów

def get_album_id():
    album_ids = set()
    for rec in [recommendations1, recommendations2, recommendations3]:
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


def create_file(album_ids):
    artist_album_dict = {}
    for album_id in album_ids:
        artists_from_album(album_id=album_id, artist_album_dict=artist_album_dict)

    album_pairs = set()
    for artist, albums in artist_album_dict.items():
        if len(albums) > 1:
            pairs = combinations(albums, 2)
            album_pairs.update(pairs)

    with open('albums_pairs.txt', 'w', encoding='utf-8') as f:
        for album1, album2 in album_pairs:
            f.write(f"{album1}, {album2}\n")

    with open('all_albums.txt', 'w', encoding='utf-8') as f:
        for id in album_ids:
            f.write(f"{sp.album(album_id=id)['name']}\n")

if __name__ == '__main__':
    album_ids = get_album_id()
    create_file(album_ids=album_ids)