from os import environ, path

from dotenv import load_dotenv

class Config:

    FLASK_ENV = 'deployment'
    FLASK_APP = 'wsgi.py'
    DEBUG = False