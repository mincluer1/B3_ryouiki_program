import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime
import csv

# Spotifyの認証情報を入力
CLIENT_ID = 'bf92708b648c4a7dae7981b0ed9f9bd1'
CLIENT_SECRET = 'dd14a04d71cf4f2587035b381862f1e9'
REDIRECT_URI = 'http://127.0.0.1:8000'

# 認証スコープ（再生履歴を取得するため）
scope = "user-read-recently-played"

# 認証処理
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope
))

# 最近再生した曲の履歴取得（最大50件）
results = sp.current_user_recently_played(limit=50)

# CSVファイルを開く（追記モード、なければ作成）
with open('spotify_recently_played.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    # ヘッダーを書き込み
    writer.writerow(['再生日時', 'アーティスト', '曲名'])
    
    # データ整形とCSV出力
    for idx, item in enumerate(results['items']):
        played_at = item['played_at']  # 再生時間 (ISO8601)
        dt_played = datetime.datetime.fromisoformat(played_at.replace('Z', '+00:00'))  # Pythonのdatetimeに変換

        track = item['track']
        track_name = track['name']
        artists = ", ".join([artist['name'] for artist in track['artists']])

        # CSVに書き込み
        writer.writerow([dt_played, artists, track_name])

        # 出力例（確認用）
        print(f"{dt_played} に {artists} - {track_name} を再生")
