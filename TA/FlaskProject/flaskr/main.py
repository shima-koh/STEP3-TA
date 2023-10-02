from flaskr import app
from flask import render_template, g
import sqlite3
from flask_bootstrap import BOOTSTRAP_VERSION, Bootstrap

from io import BytesIO
from PIL import Image
import base64
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# テーブル作成
#con.execute("CREATE TABLE Tenant(id INTEGER PRIMARY KEY, tena_name STRING, tena_stationId INTEGER)") #テナントDB
#con.execute("CREATE TABLE User(id INTEGER PRIMARY KEY, user_name STRING, pw INTEGER)") #ユーザーDB

bootstrap = Bootstrap(app)

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
    #cursor = db.cursor()

    #cursor.execute("SELECT * FROM Tenant")
    #data = cursor.fetchall()
    
    # SQLクエリを実行し、結果をデータフレームとして読み込む
    query = 'SELECT * FROM Tenant'
    df = pd.read_sql(query, db)
    
    # カーソルを閉じる
    #cursor.close()

    #Matplotlib
    fig = plt.figure()

    # -----以下の点線内は自由に変更可能-------
    x = np.linspace(0, 10, 100)
    y = x + np.random.randn(100) 
    plt.plot(x, y, label="test")
    # --------------------------------------
    img = fig_to_base64_img(fig)

    return render_template('index.html', img=img, df=df)

@app.route('/result', methods=['GET', 'POST'])
def result():
    # データベース接続を取得
    db = get_db()

    # SQLクエリを実行し、結果をデータフレームとして読み込む
    query = 'SELECT * FROM Tenant'
    df = pd.read_sql(query, db)
    

    return render_template('result.html', df=df)


if __name__ == '__main__':
    app.run(debug=True)