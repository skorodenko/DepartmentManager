import secrets


class Config:
    SECRET_KEY=secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://test:1111@localhost/test"
    SQLALCHEMY_TRACK_MODIFICATIONS = True