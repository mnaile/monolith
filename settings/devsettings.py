from settings.settings import BaseSettings
import os

class DevSettings(BaseSettings):
    DEBUG = True

    DB_NAME = os.getenv("DB_NAME", "flaskdb")
    DB_PORT = os.getenv("DB_PORT", 5432)
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_USER = os.getenv("DB_USER", "naile")

    SQLALCHEMY_DATABASE_URI = f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"