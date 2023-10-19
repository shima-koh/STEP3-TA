from flask import Flask
import os

app = Flask(__name__)

# データベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# シークレットキーの設定
app.config['SECRET_KEY'] = os.urandom(24)

from . import app