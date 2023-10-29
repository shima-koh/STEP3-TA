from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = os.urandom(24)

db = SQLAlchemy()
db.init_app(app)  # SQLAlchemyオブジェクトをappにアタッチ

from . import app