import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


# SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/postgres_test'
# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@postgres:5432/postgres'
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@db/postgres'


# SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

REMEMBER_COOCKIE_DURATION = timedelta(days=7)
