import os
from datetime import timedelta

class Config:
    #Указать здесь логин и пароль от базы Postgres
    SQLALCHEMY_DATABASE_URI = 'postgresql://<login>:<password>!@localhost:5433/vmbase'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
