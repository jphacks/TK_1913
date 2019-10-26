import os

class Default(object):
    pass

class Development(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/jph2019?charset=utf8'.format(**{
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'host': os.getenv('DB_HOST', 'localhost'),
    })
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

