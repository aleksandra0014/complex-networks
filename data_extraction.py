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
recommendations = sp.recommendations(seed_genres=['pop'], limit=100)

# Zbieranie unikalnych albumów
album_ids = [track['album']['id'] for track in recommendations['tracks']]

'''def artists_from_album(album_id, dict):
    album_info = sp.album(album_id)

    # Pobieranie utworów z albumu
    tracks = sp.album_tracks(album_id)
    all_artists = set()
    for track in tracks['items']:
        for artist in track['artists']:
            all_artists.add(artist['name'])

    dict[album_info['name']] = all_artists'''

def artists_from_album(album_id, artist_album_dict):
    album_info = sp.album(album_id)

    # Pobieranie utworów z albumu
    tracks = sp.album_tracks(album_id)
    
    for track in tracks['items']:
        for artist in track['artists']:
            artist_name = artist['name']
            # Dodaj album do listy albumów dla danego artysty
            if artist_name not in artist_album_dict:
                artist_album_dict[artist_name] = set()  # Inicjalizuj listę, jeśli artysta nie istnieje
            artist_album_dict[artist_name].add(album_info['name'])


artist_album_dict = {}
for album_id in album_ids:
    artists_from_album(album_id=album_id, artist_album_dict=artist_album_dict)


album_pairs = set()
for artist, albums in artist_album_dict.items():
    if len(albums) > 1:  # Sprawdź, czy artysta występuje na więcej niż jednym albumie
        pairs = combinations(albums, 2)  # Tworzy pary albumów
        album_pairs.update(pairs)

with open('albums.txt', 'w', encoding='utf-8') as f:
    for album1, album2 in album_pairs:
        f.write(f"{album1}, {album2}\n")