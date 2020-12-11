from os import environ, path


class Config:

    FLASK_ENV = 'deployment'
    FLASK_APP = 'wsgi.py'
    DEBUG = False