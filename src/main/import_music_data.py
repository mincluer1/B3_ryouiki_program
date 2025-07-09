import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime
import csv

CLIENT_ID = 'bf92708b648c4a7dae7981b0ed9f9bd1'
CLIENT_SECRET = 'dd14a04d71cf4f2587035b381862f1e9'
REDIRECT_URI = 'http://127.0.0.1:8000'

scope = "user-read-recently-played"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope
))

results = sp.current_user_recently_played(limit=50)

with open('spotify_recently_played.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    writer.writerow(['再生日時', 'アーティスト', '曲名'])
    
    for idx, item in enumerate(results['items']):
        played_at = item['played_at']
        dt_played = datetime.datetime.fromisoformat(played_at.replace('Z', '+00:00'))

        track = item['track']
        track_name = track['name']
        artists = ", ".join([artist['name'] for artist in track['artists']])

        writer.writerow([dt_played, artists, track_name])

        print(f"{dt_played} に {artists} - {track_name} を再生")
