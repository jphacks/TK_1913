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
    MQTT_BROKER_URL = 'localhost'
    MQTT_BROLER_PORT = 1883
    MQTT_USERNAME = 'flask'
    MQTT_PASSWORD = 'secret'
    MQTT_REFRESH_TIME = 1.0
    MQTT_TOPIC = 'topic'

