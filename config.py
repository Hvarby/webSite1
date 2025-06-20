import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mysecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///staff.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False