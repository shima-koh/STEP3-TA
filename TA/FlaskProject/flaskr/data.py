import sqlite3
import numpy as np
import pandas as pd

# データベースファイルのパス
DATABASE = 'app.db'


def get_db():
    # グローバルなデータベース接続がすでに存在する場合、それを返す
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db


# テーブル作成
#con.execute("CREATE TABLE Tenant(id INTEGER PRIMARY KEY, tena_name STRING, tena_stationId INTEGER)") #テナントDB
#con.execute("CREATE TABLE User(id INTEGER PRIMARY KEY, user_name STRING, pw INTEGER)") #ユーザーDB

