
import os
import secrets
from dotenv import load_dotenv
load_dotenv()


USER = os.environ.get("MYSQL_USER")
PASSWORD = os.environ.get("MYSQL_PASSWORD")
SERVER = os.environ.get("MYSQL_SERVER")
DATABASE = os.environ.get("MYSQL_DATABASE")


class Config:
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{USER}:{PASSWORD}@{SERVER}/{DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
