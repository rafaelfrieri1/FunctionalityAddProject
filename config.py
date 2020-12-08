from os import environ, path

from dotenv import load_dotenv

class Config:

    FLASK_ENV = 'development'
    FLASK_APP = 'wsgi.py'
    DEBUG = True