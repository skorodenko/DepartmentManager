
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


MIGRATIONS_DIRECTORY = os.path.join("department_app", "migrations")

app = Flask(__name__)
app.config.from_mapping(
    DEBUG=True,
    SECRET_KEY="dev",
    SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://rinkuro:1111@localhost/test",
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
)


db = SQLAlchemy(app)
migrate = Migrate(app, db, directory=MIGRATIONS_DIRECTORY)
