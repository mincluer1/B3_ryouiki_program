import pandas as pd
from datetime import datetime
from surprise import Dataset, Reader, KNNBasic

# CSV読み込み
df = pd.read_csv('spotify_recently_played.csv')

# 時間帯を分類する関数
def get_time_slot(dt_str):
    hour = pd.to_datetime(dt_str).hour
    if 6 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 18:
        return 'afternoon'
    elif 18 <= hour < 24:
        return 'evening'
    else:
        return 'night'

df['time_slot'] = df['再生日時'].apply(get_time_slot)

# 現在の時間帯を決定
now = datetime.now()
current_hour = now.hour

if 6 <= current_hour < 12:
    time_slot = 'morning'
elif 12 <= current_hour < 18:
    time_slot = 'afternoon'
elif 18 <= current_hour < 24:
    time_slot = 'evening'
else:
    time_slot = 'night'

print(f"現在時刻: {now.strftime('%Y-%m-%d %H:%M:%S')} → 時間帯: '{time_slot}'")

# =======================
# アーティスト推薦
# =======================
grouped_artist = df.groupby(['time_slot', 'アーティスト']).size().reset_index(name='play_count')

reader_artist = Reader(rating_scale=(1, grouped_artist['play_count'].max()))
data_artist = Dataset.load_from_df(grouped_artist[['time_slot', 'アーティスト', 'play_count']], reader_artist)

trainset_artist = data_artist.build_full_trainset()
model_artist = KNNBasic(sim_options={'user_based': True})
model_artist.fit(trainset_artist)

all_items_artist = trainset_artist.all_items()
all_artists = [trainset_artist.to_raw_iid(iid) for iid in all_items_artist]
listened_artists = grouped_artist[grouped_artist['time_slot'] == time_slot]['アーティスト'].tolist()
candidates_artists = [artist for artist in all_artists if artist not in listened_artists]

predictions_artist = [model_artist.predict(time_slot, artist) for artist in candidates_artists]

if predictions_artist:
    best_artist = max(predictions_artist, key=lambda x: x.est)
    print(f"\n🎤 現在の時間帯 '{time_slot}' に最もおすすめのアーティスト:")
    print(f"{best_artist.iid} (予測再生スコア: {best_artist.est:.2f})")
else:
    print("\n🎤 十分なデータがなく、アーティストのおすすめを生成できませんでした。")

# =======================
# 曲名推薦（トップ5）
# =======================
grouped_song = df.groupby(['time_slot', '曲名']).size().reset_index(name='play_count')

reader_song = Reader(rating_scale=(1, grouped_song['play_count'].max()))
data_song = Dataset.load_from_df(grouped_song[['time_slot', '曲名', 'play_count']], reader_song)

trainset_song = data_song.build_full_trainset()
model_song = KNNBasic(sim_options={'user_based': True})
model_song.fit(trainset_song)

all_items_song = trainset_song.all_items()
all_songs = [trainset_song.to_raw_iid(iid) for iid in all_items_song]
listened_songs = grouped_song[grouped_song['time_slot'] == time_slot]['曲名'].tolist()
candidates_songs = [song for song in all_songs if song not in listened_songs]

predictions_song = [model_song.predict(time_slot, song) for song in candidates_songs]

if predictions_song:
    top5_songs = sorted(predictions_song, key=lambda x: x.est, reverse=True)[:5]
    print(f"\n🎵 現在の時間帯 '{time_slot}' におすすめの曲 トップ5:")
    for i, pred in enumerate(top5_songs, 1):
        print(f"{i}. {pred.iid} (予測再生スコア: {pred.est:.2f})")
else:
    print("\n🎵 十分なデータがなく、曲のおすすめを生成できませんでした。")
