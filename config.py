import os


class Config(object):
    SECRET_KEY = os.environ.get('SECTRE_KEY') or 'never-everr'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///fmarket.db'
