from flaskr import app
from flask import render_template, g, request, redirect, jsonify
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash


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

# データベースファイルのパス
DATABASE = 'app.db'
# データベース接続を取得
db = get_db()

def get_db():
    # グローバルなデータベース接続がすでに存在する場合、それを返す
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

with app.app_context():
    data = SomeModel.query.all()

with app.app_context():
    new_data = SomeModel(some_field='some_value')
    db.session.add(new_data)
    db.session.commit()

with app.app_context():
    data_to_update = SomeModel.query.get(some_id)
    data_to_update.some_field = 'new_value'
    db.session.commit()

with app.app_context():
    data_to_delete = SomeModel.query.get(some_id)
    db.session.delete(data_to_delete)
    db.session.commit()





login_manager = LoginManager()
login_manager.init_app(app)



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(12))

# アプリケーションコンテキストを設定する
@app.before_request
def before_request():
    g.db = get_db()  # データベース接続を取得


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User(username=username, password=generate_password_hash(password, method='sha256'))

        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# テーブル作成
#con.execute("CREATE TABLE Tenant(id INTEGER PRIMARY KEY, tena_name STRING, tena_stationId INTEGER)") #テナントDB
#con.execute("CREATE TABLE User(id INTEGER PRIMARY KEY, user_name STRING, pw INTEGER)") #ユーザーDB



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

    initial_investment = request.form.get('initial_investment')
    if initial_investment is None or initial_investment.strip() == '':
        initial_investment = 2000000
        print("デフォルト値を設定しましたInvest")
    else:
        initial_investment = float(request.form.get('initial_investment'))
        initial_investment = initial_investment * 10000

    bussiness_hour = request.form.get('bussiness_hour')
    if  bussiness_hour is None or bussiness_hour.strip() == '':
        bussiness_hour = 10
        print("デフォルト値を設定しましたbusinessh")
    else:
        bussiness_hour = int(request.form.get('bussiness_hour'))
    
    ave_time = request.form.get('ave_time')
    if ave_time is None or ave_time.strip() == '':
        ave_time = 90
        print("デフォルト値を設定しましたtime")
    else:
        ave_time = int(request.form.get('ave_time'))
        
    chair = request.form.get('chair') 
    if chair is None or chair.strip() == '':
        chair = 2
        print("デフォルト値を設定しましたchair")
    else:
        chair = int(request.form.get('chair'))
    
    booking_rate = request.form.get('booking_rate') 
    if booking_rate is None or booking_rate.strip() == '':
        booking_rate = 60
        print("デフォルト値を設定しましたrate")
    else:    
        booking_rate = int(request.form.get('booking_rate'))

    days = request.form.get('days')
    if  days is None or days.strip() == '':
        days = 25
        print("デフォルト値を設定しましたdays")
    else:
        days = int(request.form.get('days'))

    customer_price = request.form.get('customer_price')
    if customer_price is None or customer_price.strip() == '':
        customer_price = 5000
        print("デフォルト値を設定しましたprice")
    else:
        customer_price = int(request.form.get('customer_price'))
    
    movingin_cost = request.form.get(' movingin_cost')
    if movingin_cost is None or movingin_cost.strip() == '':
        movingin_cost = 6
        print("デフォルト値を設定しましたin")
    else:
        movingin_cost = int(request.form.get(' movingin_cost'))
    
    moving_cost = request.form.get('moving_cost')
    if moving_cost is None or moving_cost.strip() == '':
        moving_cost = 500000
        print("デフォルト値を設定しましたmove")
    else:
        moving_cost = int(request.form.get('moving_cost'))
    
    rent_cost = request.form.get('rent_cost')
    if rent_cost is None or rent_cost.strip() == '':
        rent_cost = df_rent["tena_rent"][0]
        print("デフォルト値を設定しましたrent")
    else:
        rent_cost = int(request.form.get('rent_cost'))
    
    hire_cost = request.form.get('hire_cost')
    if hire_cost is None or hire_cost.strip() == '':
        hire_cost = 3
        print("デフォルト値を設定しましたhire")
    else:
        hire_cost = int(request.form.get('hire_cost'))

    utility_cost = request.form.get('utility_cost')
    if utility_cost is None or utility_cost.strip() == '':
        utility_cost = 5000
        print("デフォルト値を設定しましたutil")
    else:
        utility_cost = float(request.form.get('utility_cost'))
    
    material_cost = request.form.get('material_cost')
    if material_cost is None or material_cost.strip() == '':
        material_cost = .2
        print("デフォルト値を設定しましたmeter")
    else:
        material_cost = float(request.form.get('material_cost'))
    
    ad_cost = request.form.get('ad_cost')
    if ad_cost is None or ad_cost.strip() == '':
        ad_cost = 100000
        print("デフ入れるADno")
    else:
        ad_cost = int(request.form.get('ad_cost'))

    bussiness_minutes = 60

    max_turnover = float(bussiness_hour) * float(bussiness_minutes) / float(ave_time)

    if max_turnover is not None:
        max_turnover_str = str(max_turnover)
        print("回転計さんturn" + max_turnover_str)
    else:
        print("max_turnoverはNoneです。")

    servicenum = chair * max_turnover * (booking_rate/100)
    print("回転計さん"+  str(servicenum))
    benefit = servicenum * customer_price * days
    benefit = int(benefit)
    print("回転計さん"+  str(benefit))

    initial_cost =  movingin_cost + moving_cost
    print("回転計さんinitial"+  str(initial_cost))
    print("回転計さんInvest"+  str(initial_investment))

    if ( (initial_investment - initial_cost) >= 0 ):
        initial_check =  "Clear"
    else:
        initial_check = int(initial_investment) - int(initial_cost)
    

    fixed_cost =   rent_cost + (hire_cost * 350000) + utility_cost
    print("回転計さん"+  str(fixed_cost))
    variable_cost = ( benefit * (material_cost/100)) + ad_cost
    variable_cost = int(variable_cost)
    print("回転計さん"+  str(variable_cost))

    final_benefit = benefit - (fixed_cost + variable_cost)
    final_benefit = int(final_benefit)
    print("Final:--------------------"+ str(final_benefit))

    initial_investment = initial_investment /10000

    #計算のデータをディクショナリにまとめる
    result_data = {
        'initial_investment': initial_investment,
        'bussiness_hour': bussiness_hour,
        'bussiness_minutes': bussiness_minutes,
        'ave_time':ave_time,
        'max_turnover': max_turnover,
        'servicenum':servicenum,
        'chair':chair,
        'booking_rate':booking_rate,
        'benefit':benefit,
        'customer_price':customer_price,
        'days':days,
        'initial_cost':initial_cost,
        'movingin_cost':movingin_cost,
        'moving_cost':moving_cost,
        
        'initial_check':initial_check,
        
        'fixed_cost':fixed_cost,
        'rent_cost':rent_cost,
        'hire_cost':hire_cost,
        'utility_cost':utility_cost,
        'variable_cost':variable_cost,
        'material_cost':material_cost,
        'ad_cost':ad_cost,
        'final_benefit': final_benefit,  # ここに最終結果を追加
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
