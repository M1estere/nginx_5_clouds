import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class Config:

    FLASK_APP = "app.py"
    FLASK_APP_HOST = os.getenv("FLASK_APP_HOST")
    FLASK_APP_PORT = os.getenv("FLASK_APP_PORT")
    # FLASK_DEBUG = os.getenv("FLASK_DEBUG")
    FLASK_DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")

    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = os.getenv("REDIS_HOST")
    CACHE_REDIS_PORT = os.getenv("REDIS_PORT")
    CACHE_REDIS_DB = os.getenv("REDIS_DB")
    CACHE_REDIS_URL = f"redis://{CACHE_REDIS_HOST}:{CACHE_REDIS_PORT}/{CACHE_REDIS_DB}"


settings = Config
