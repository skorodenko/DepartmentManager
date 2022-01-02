
import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


MIGRATIONS_DIRECTORY = os.path.join("department_app", "migrations")

app = Flask(__name__)
app.config.from_mapping(
    TESTING=True,
    ENV="development",
    SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://test:1111@localhost/test",
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
)

api = Api(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db, directory=MIGRATIONS_DIRECTORY)


from .rest import init_rest
init_rest()
