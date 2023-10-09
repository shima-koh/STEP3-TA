import sqlite3
import numpy as np
import pandas as pd
import requests 

# データベースファイルのパス
DATABASE = 'app.db'

conn = sqlite3.connect(DATABASE) 


# テーブル作成
#conn.execute("CREATE TABLE Tenant(id INTEGER PRIMARY KEY, tena_name STRING, tena_stationId INTEGER)") #テナントDB
#conn.execute("CREATE TABLE User(id INTEGER PRIMARY KEY, user_name STRING, pw INTEGER)") #ユーザーDB


# データフレームをSQLiteデータベースに書き込む
table_name = '店舗一覧'  # テーブル名を適切なものに変更してください

#df.to_sql(table_name, conn, if_exists='replace', index=False)

        # jSTAT MAP認証設定
REQUEST_URL = 'https://jstatmap.e-stat.go.jp/statmap/api/1.00?category=richReport&func=getSummary'
USER_ID = '&userid=noriyasukawana@outlook.jp'  #個人の登録ID
API_KEY = '&key=dMUbbbyc9ThTzG4PNpA2'  #個人のAPIキー
        # params入力設定
rangeType = '&rangeType=circle'  # circle(円) or driveTime(到達圏)
travelMode = '&travelMode=walking'  # car(車) or walking(徒歩)
speed = '&speed=3.2'  # 時速(km/h)
time = '&time=15,30,45'  # 移動時間(min)
output = '&output=json'  # 出力形式
radius = '&radius=500'
        # 空のdfを用意
df9 = pd.DataFrame()

latitude = '&lat=' + str(35.675069)  # 緯度
longitude = '&lng=' + str(139.763332)  # 経度
res = requests.get(REQUEST_URL + USER_ID + latitude + longitude + rangeType + radius + API_KEY + output)
res.json()
result = res.json() 

print(result)


