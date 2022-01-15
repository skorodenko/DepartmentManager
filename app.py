from department_app import init_app


class DevConfig:
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://test:1111@localhost/test"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

init_app(DevConfig)
from department_app import app

if __name__ == "__main__":
    app.run()