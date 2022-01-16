# pylint: disable=wrong-import-position,invalid-name,global-variable-undefined,import-outside-toplevel
"""
Contains factory to initialize web application and web service
"""

import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


MIGRATIONS_DIRECTORY = os.path.join("department_app", "migrations")


def init_app(test_config=None):
    # These objects are global to use different 
    # databases for tests 
    # (mysql for prod, sqlite in memory for tests)
    # and keep project structure simple and fancy.
    global app, api, db, migrate

    app = Flask(__name__)

    if test_config is None:
        from config import Config
        app.config.from_object(Config)
    else:
        app.config.from_object(test_config)

    api = Api(app)

    db = SQLAlchemy(app)

    migrate = Migrate(app, db, directory=MIGRATIONS_DIRECTORY)

    from .rest import init_rest
    init_rest()

    from .views import init_views
    init_views()

    return app
