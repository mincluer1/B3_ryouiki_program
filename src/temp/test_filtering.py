import pandas as pd
from datetime import datetime
from surprise import Dataset, Reader, KNNBasic

# CSVファイルを読み込み
df = pd.read_csv('spotify_recently_played.csv')  # 再生日時, アーティスト, 曲名

# 時間帯を分類（擬似的にユーザーとみなす）
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

# 曲またはアーティスト単位で集計（ここではアーティストにする）
grouped = df.groupby(['time_slot', 'アーティスト']).size().reset_index(name='play_count')

# Surprise用データ整形
reader = Reader(rating_scale=(1, grouped['play_count'].max()))
data = Dataset.load_from_df(grouped[['time_slot', 'アーティスト', 'play_count']], reader)

# 協調フィルタリングモデル（時間帯間の嗜好の類似度を見る）
trainset = data.build_full_trainset()
model = KNNBasic(sim_options={'user_based': True})
model.fit(trainset)

# 🌞 現在の時間帯を自動判定
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

# アーティスト一覧
all_items = trainset.all_items()
all_artists = [trainset.to_raw_iid(iid) for iid in all_items]

# すでに聴いたアーティスト
listened = grouped[grouped['time_slot'] == time_slot]['アーティスト'].tolist()

# 推薦候補（その時間帯に未再生）
candidates = [artist for artist in all_artists if artist not in listened]

# 推薦スコアを算出
predictions = [model.predict(time_slot, artist) for artist in candidates]

# 最もスコアが高いアーティストのみを表示
if predictions:
    best_recommendation = max(predictions, key=lambda x: x.est)
    print(f"\n🎧 現在の時間帯 '{time_slot}' に最もおすすめのアーティスト:")
    print(f"{best_recommendation.iid} (予測再生スコア: {best_recommendation.est:.2f})")
else:
    print("\n十分なデータがなく、現在の時間帯におすすめを生成できませんでした。")
