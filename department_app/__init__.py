
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_mapping(
    DEBUG=True,
    SECRET_KEY="dev",
    SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://rinkuro:1111@localhost/test",
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
)


db = SQLAlchemy(app)
