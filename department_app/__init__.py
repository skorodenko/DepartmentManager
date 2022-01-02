
import os
import secrets
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


MIGRATIONS_DIRECTORY = os.path.join("department_app", "migrations")


def create_app(test_config=None):
    
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=secrets.token_hex(16)
    )

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.from_object(test_config)

    return app


class DEV_CONFIG:
    ENV="development"
    SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://test:1111@localhost/test"
    SQLALCHEMY_TRACK_MODIFICATIONS=True

app = create_app(DEV_CONFIG)

api = Api(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db, directory=MIGRATIONS_DIRECTORY)

from .rest import init_rest
init_rest(api)
