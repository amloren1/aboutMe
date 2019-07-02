import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True