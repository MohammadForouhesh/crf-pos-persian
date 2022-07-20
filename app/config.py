from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.join(path.dirname(__file__), '..'))
# loading env vars from .env file
load_dotenv()


class BaseConfig(object):
    ''' Base config class. '''

    APP_NAME = environ.get('APP_NAME') or 'crf-pos'
    ORIGINS = ['*']
    EMAIL_CHARSET = 'UTF-8'
    API_KEY = environ.get('API_KEY')
    BROKER_URL = environ.get('BROKER_URL')
    RESULT_BACKEND = environ.get('RESULT_BACKEND')

    FIRSTH = 60
    SECONDTH = 90

class Development(BaseConfig):
    ''' Development config. '''

    DEBUG = False
    ENV = 'dev'

class Staging(BaseConfig):
    ''' Staging config. '''

    DEBUG = False
    ENV = 'staging'


class Production(BaseConfig):
    ''' Production config '''

    DEBUG = False
    ENV = 'production'


config = {
    'development': Development,
    'staging': Staging,
    'production': Production,
}
