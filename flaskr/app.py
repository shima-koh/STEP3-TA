from flaskr import app
from flask import render_template, g, request, redirect, jsonify
import sqlite3
from io import BytesIO
from PIL import Image
import base64
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json

import folium
from folium.plugins import HeatMap


# テーブル作成
#con.execute("CREATE TABLE Tenant(id INTEGER PRIMARY KEY, tena_name STRING, tena_stationId INTEGER)") #テナントDB
#con.execute("CREATE TABLE User(id INTEGER PRIMARY KEY, user_name STRING, pw INTEGER)") #ユーザーDB



# データベースファイルのパス
DATABASE = 'app.db'

def get_db():
    # グローバルなデータベース接続がすでに存在する場合、それを返す
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

# -----figをbase64形式に変換を関数化------
def fig_to_base64_img(fig):
    io = BytesIO()
    fig.savefig(io, format="png")
    io.seek(0)
    base64_img = base64.b64encode(io.read()).decode()

    return base64_img

@app.teardown_appcontext
def close_db(error):
    # リクエストの終了時にデータベース接続をクローズ
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    # データベース接続を取得
    db = get_db()
    # SQLクエリを実行し、結果をデータフレームとして読み込む
    query = 'SELECT * FROM Tenant'
    df = pd.read_sql(query, db)
    
    query = 'SELECT * FROM Station'
    df_station = pd.read_sql(query, db)

    #Matplotlib
    fig = plt.figure()

    # -----以下の点線内は自由に変更可能-------
    x = np.linspace(0, 10, 100)
    y = x + np.random.randn(100) 
    plt.plot(x, y, label="test")
    # --------------------------------------
    img = fig_to_base64_img(fig)

    return render_template('index.html', img=img, df=df,df_station=df_station)



@app.route('/result', methods=['GET', 'POST'])
def result():

    # もしPOSTメソッドならresult.htmlに値dfと一緒に飛ばす
    if request.method == 'POST':
        # データベース接続を取得
        db = get_db()

        # HTMLでセレクトした駅情報を取得
        station_num = request.form.get('selected_option')
        

        if station_num is not None:
            # Tena_StationIdがStation_Numと一致するテナントデータを取得し、DataFrameに読み込む
            query = f"SELECT * FROM Tenant WHERE Tena_StationId={station_num}"
            df_rent = pd.read_sql(query, db)

            query = f"SELECT * FROM Station WHERE stationId={station_num}"
            df_area = pd.read_sql(query, db)

            #Map情報の取得
            station_name = df_area["stationName"][0]
            station_lat = df_area["lat"][0]
            station_lon = df_area["lon"][0]


            map = folium.Map(location=[station_lat, station_lon],zoom_start = 15,tiles='OpenStreetMap') 

            #MapへのCircle表示
            en = folium.Circle(
            location=[station_lat, station_lon], # 中心
            radius=100, # 半径100m
            color='#ff0000', # 枠の色
            fill_color='#0000ff' # 塗りつぶしの色
            )
            en.add_to(map)

            marker = folium.Marker([station_lat, station_lon], popup=station_name)
            marker.add_to(map)

            if not df_rent.empty:
                # 結果をHTMLテンプレートに渡す
                return render_template('result.html',df_area=df_area, df_rent=df_rent, map_html=map._repr_html_())
            else:
                return 'No tenant data found for the selected station.'
        else:
            return f'StationNum for {station_num} not found'
    
    # POSTメソッドカードセレクトとして飛ばす
    else:
        return render_template("index.html")





@app.route('/rent_info', methods=['GET', 'POST'])
def rent_info():

    card_id = card_id = request.form.get('card_info')

    # POSTリクエストから直接値を取得
    card_id = request.form.get('card_info')
    print(card_id)

    db = get_db()

    # Tena_StationIdがStation_Numと一致するテナントデータを取得し、DataFrameに読み込む
    query = f"SELECT * FROM Tenant WHERE id={card_id}"
    df_rent = pd.read_sql(query, db)
        
    # ここでカード情報を扱う処理を行う

    # レンダリングするHTMLを指定して表示
    return render_template('rent_info.html', df_rent=df_rent)  # GeoInfoページのHTMLテンプレート名を指定
        


@app.route('/GeoInfo', methods=['GET', 'POST'])
def GeoInfo():
    # POSTリクエストから直接値を取得
    card_id = request.form.get('card_info')
    print(card_id)

    db = get_db()

    # Tena_StationIdがStation_Numと一致するテナントデータを取得し、DataFrameに読み込む
    query = f"SELECT * FROM Tenant WHERE id={card_id}"
    df_rent = pd.read_sql(query, db)

    station_num = df_rent["tena_stationId"][0]
    print(station_num)

    query = f"SELECT * FROM Tenant WHERE Tena_StationId={station_num}"
    df_rent = pd.read_sql(query, db)

    query = f"SELECT * FROM Station WHERE stationId={station_num}"
    df_area = pd.read_sql(query, db)

            #Map情報の取得
    station_name = df_area["stationName"][0]
    station_lat = df_area["lat"][0]
    station_lon = df_area["lon"][0]


    map = folium.Map(location=[station_lat, station_lon],zoom_start = 15,tiles='OpenStreetMap') 

    #MapへのCircle表示
    en = folium.Circle(
    location=[station_lat, station_lon], # 中心
    radius=800, # 半径100m
    color='#ff0000', # 枠の色
    fill_color='#0000ff' # 塗りつぶしの色
    )
    en.add_to(map)

    marker = folium.Marker([station_lat, station_lon], popup=station_name)
    marker.add_to(map)
    
    # ここでカード情報を扱う処理を行う

    # レンダリングするHTMLを指定して表示
    return render_template('GeoInfo.html', df_rent=df_rent,map_html=map._repr_html_())  # GeoInfoページのHTMLテンプレート名を指定



@app.route('/calc', methods=['GET', 'POST'])
def calc():

    # POSTリクエストから直接値を取得
    card_id = request.form.get('card_info')
    print(card_id)
    if card_id is None:
        card_id = request.form.get('card_id')

    db = get_db()

    # Tena_StationIdがStation_Numと一致するテナントデータを取得し、DataFrameに読み込む
    query = f"SELECT * FROM Tenant WHERE id={card_id}"
    df_rent = pd.read_sql(query, db)

    if request.form.get('initialInvestment') is None:
        initialInvestment = 200
    else:
        initialInvestment = request.form.get('initialInvestment')
    
    if request.form.get('bussiness_hour') is None:
        bussiness_hour = 10
    else:
        bussiness_hour = request.form.get('bussiness_hour')
    
    if request.form.get('ave_time') is None:
        ave_time = 90
    else:
        ave_time = request.form.get('ave_time')
        
    if request.form.get('chair') is None:
        chair = 2
    else:
        chair = request.form.get('chair')
    
    if request.form.get('booking_rate') is None:
        booking_rate = .6
    else:    
        booking_rate = request.form.get('booking_rate')

    if  request.form.get('days') is None:
        days = 25
    else:
        days = request.form.get('days')

    if request.form.get('customer_price') is None:
        customer_price = 5000
    else:
        customer_price = request.form.get('customer_price')
    
    if request.form.get(' movingin_cost') is None:
        movingin_cost = 6
    else:
        movingin_cost = request.form.get(' movingin_cost')
    
    if request.form.get('moving_cost') is None:
        moving_cost = 500000
    else:
        moving_cost = request.form.get('moving_cost')
    
    if request.form.get('initial_cost') is None:
        initial_cost = 0
    else:
        initial_cost = request.form.get('initial_cost')
    
    if request.form.get('rent_cost') is None:
        rent_cost = 15
    else:
        rent_cost = request.form.get('rent_cost')
    
    if request.form.get('hire_cost') is None:
        hire_cost = 500000
    else:
        hire_cost = request.form.get('hire_cost')

    if request.form.get('utility_cost') is None:
        utility_cost = .1
    else:
        utility_cost = request.form.get('utility_cost')
    
    if request.form.get('material_cost') is None:
        material_cost = .2
    else:
        material_cost = request.form.get('material_cost')
    
    if request.form.get('ad_cost') is None:
        ad_cost = 100000
    else:
        ad_cost = request.form.get('ad_cost')

    max_turnover = bussiness_hour * 60 / ave_time
    servicenum = chair * max_turnover * booking_rate
    benefit = servicenum * customer_price * days

    initial_cost =  movingin_cost + moving_cost
    if ( (initialInvestment - initial_cost) >= 0 ):
        initial_check =  "Clear"
    else:
        initial_check = initialInvestment - initial_cost
    

    fixed_cost =   rent_cost + (hire_cost * 350000) + utility_cost
    variable_cost = ( benefit * material_cost) + ad_cost

    final_benefit = benefit - fixed_cost - variable_cost

    ave_time = 200
    #計算のデータをディクショナリにまとめる
    result_data = {
        'initialInvestment': initialInvestment,
        'bussiness_hour': bussiness_hour,
        'ave_time':ave_time,
        # 他のデータも同様に追加
        'final_benefit': final_benefit  # ここに最終結果を追加
    }

    # レンダリングするHTMLを指定して表示
    return render_template('calc.html', df_rent=df_rent, df_calc=result_data)  # GeoInfoページのHTMLテンプレート名を指定


"""
@app.route('/map', methods=['GET', 'POST'])
def map():

    if request.method == 'POST':
        # データベース接続を取得
        db = get_db()
        # HTMLでセレクトした駅情報を取得
        station_num = request.form.get('selected_option')

        if station_num is not None:
            cursor = db.cursor()
            cursor.execute('SELECT stationName FROM Station WHERE stationId=?', station_num)
            station_name = cursor.fetchone()
            cursor.execute('SELECT lat FROM Station WHERE stationId=?', station_num)
            station_lat = cursor.fetchone()
            cursor.execute('SELECT lon FROM Station WHERE stationId=?', station_num)
            station_lon = cursor.fetchone()

            # カーソルを閉じる
            cursor.close()

            map = folium.Map(location=[station_lat[0], station_lon[0]],zoom_start = 15,tiles='OpenStreetMap') 

            #MapへのCircle表示
            en = folium.Circle(
            location=[station_lat[0], station_lon[0]], # 中心
            radius=100, # 半径100m
            color='#ff0000', # 枠の色
            fill_color='#0000ff' # 塗りつぶしの色
            )
            en.add_to(map)

            marker = folium.Marker([station_lat[0], station_lon[0]], popup=station_name[0])
            marker.add_to(map)
            return map._repr_html_()
    """

if __name__ == '__main__':
    app.run(debug=True)
