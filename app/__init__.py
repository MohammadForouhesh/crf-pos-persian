from os import environ

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from .config import config as app_config


def create_app():
    # loading env vars from .env file
    load_dotenv()
    APPLICATION_ENV = get_environment()
    app = Flask(app_config[APPLICATION_ENV].APP_NAME)
    app.config.from_object(app_config[APPLICATION_ENV])

    CORS(app, resources={r'/api/*': {'origins': '*'}})

    return app


def get_environment():
    return environ.get('APPLICATION_ENV') or 'development'
