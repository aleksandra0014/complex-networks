import re
import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import pandas as pd


def get_playlist_link():
    playlists = []
    try:
        with open(r'C:\Users\aleks\OneDrive\Documents\SIECI_ZLOZONE\src\playlists.txt', 'r') as f:
            for line in f:
                playlists.append(line.strip())  # Usuwamy zbędne białe znaki
    except Exception as e:
        print(f"Błąd przy odczycie pliku playlists.txt: {e}")
    return playlists


def get_lists(playlist_tracks):
    tracks_name = set()
    tracks_id = set()
    artist_id = set()
    artist_name = set()
    dic_artist_track = dict()

    # Słowniki na popularność i gatunki
    track_popularity = {}
    artist_popularity = {}
    artist_genres = {}

    for item in playlist_tracks:
        track = item.get('track')
        if not track:
            continue

        try:
            # Dodawanie nazw i ID utworów
            tracks_name.add(track.get('name', ''))
            tracks_id.add(track.get('id', ''))

            # Popularność piosenek
            track_popularity[track.get('name', '')] = track.get('popularity', 0)

            # Przetwarzanie artystów
            for artist in track.get('artists', []):
                artist_name_value = artist.get('name', None)
                if artist_name_value is None:
                    continue  # Pomijamy artystów, których nazwa jest None
                
                artist_name.add(artist_name_value)
                artist_id.add(artist.get('id', ''))

                try:
                    # Pobieranie szczegółowych informacji o artyście
                    artist_info = sp.artist(artist.get('id'))  # Zapytanie do API Spotify o szczegóły artysty
                    artist_popularity[artist_name_value] = artist_info.get('followers', {}).get('total', 0)

                    # Pobieranie gatunków artystów
                    artist_genres[artist_name_value] = artist_info.get('genres', [])

                except Exception as e:
                    # Obsługuje wyjątek, jeśli nie uda się pobrać danych o artyście
                    print(f"Nie udało się pobrać informacji o artyście {artist_name_value}: {str(e)}")
                    artist_popularity[artist_name_value] = None  # Możemy przypisać None
                    artist_genres[artist_name_value] = []  # Pusta lista gatunków

            # Mapowanie nazwy utworu do listy artystów
            dic_artist_track[track.get('name', '')] = [
                artist.get('name', '') for artist in track.get('artists', []) if artist.get('name') is not None
            ]
        
        except Exception as e:
            # Obsługuje wyjątek, jeśli nie uda się przetworzyć informacji o utworze
            print(f"Nie udało się przetworzyć utworu {track.get('name', '')}: {str(e)}")
            continue  # Przechodzi do następnego utworu


    return tracks_id, tracks_name, artist_id, artist_name, dic_artist_track, track_popularity, artist_popularity, artist_genres


def get_df(tracks_name, artist_name, track_popularity, artist_followers, artist_genres):
    print('Funckja df')
    track_df = pd.DataFrame(list(track_popularity.items()), columns=['track_name', 'track_popularity'])
    artist_df = pd.DataFrame(list(artist_followers.items()), columns=['artist_name', 'artist_followers'])
    artist_df['genres'] = artist_df['artist_name'].map(artist_genres)
    track_df.to_csv(r'C:\Users\aleks\OneDrive\Documents\SIECI_ZLOZONE\data\df\track_df2.csv', mode='a', header=False, index=False)
    artist_df.to_csv(r'C:\Users\aleks\OneDrive\Documents\SIECI_ZLOZONE\data\df\artist_df2.csv', mode='a', header=False, index=False)
    print('Zapisano df')

def create_file_for_bipartite_graph(tracks_name, artist_name, dic_artist_track, file_artist, file_tracks, file_pais):
    pairs_set = set()

    # Generowanie par (utwór, artysta) tylko dla artystów, których nazwa nie jest None
    for track, artists in dic_artist_track.items():
        for artist in artists:
            if artist is not None:  # Sprawdzamy, czy artysta ma nazwę różną od None
                pairs_set.add(f"{track}; {artist}")

    # Zapis danych do plików
    try:
        with open(file_artist, 'a', encoding='utf-8') as f:
            for artist in artist_name:
                if artist is not None:
                    f.write(f'{artist}\n')

        with open(file_tracks, 'a', encoding='utf-8') as f:
            for track in tracks_name:
                if track is not None:
                    f.write(f'{track}\n')

        with open(file_pais, 'a', encoding='utf-8') as f:
            for pair in pairs_set:
                f.write(f'{pair}\n')

        print('Zaaktualizowano pliki')

    except Exception as e:
        print(f"Coś poszło nie tak przy zapisywaniu plików: {e}")

if __name__ == '__main__':


    load_dotenv()

    # Uwierzytelnianie Spotify API
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Pobieranie playlisty
    playlist_list = get_playlist_link()
    for playlist_url in playlist_list:
        match = re.search(r'playlist/([a-zA-Z0-9]+)', playlist_url)
        if not match:
            raise ValueError("Invalid playlist URL format.")
        playlist_id = match.group(1)

        # Pobieranie wszystkich utworów z playlisty
        playlist_tracks = []
        offset = 0
        while True:
            response = sp.playlist_tracks(playlist_id, offset=offset)
            playlist_tracks.extend(response['items'])
            if not response['next']:
                break
            offset += len(response['items'])
        print(f"Fetched {len(playlist_tracks)} tracks from playlist.")

        tracks_id, tracks_name, artist_id, artist_name, dic_artist_track, track_popularity, artist_followers, artist_genres = get_lists(playlist_tracks)
        get_df(tracks_name, artist_name, track_popularity, artist_followers, artist_genres)
        # Tworzenie plików dla grafu bipartytnego
        create_file_for_bipartite_graph(
            tracks_name,
            artist_name,
            dic_artist_track,
            'data/data_project/artists2.txt',
            'data/data_project/tracks2.txt',
            'data/data_project/pairs2.txt'
        )
