import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


# SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/poor_trip_test'
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@db/postgres'


SQLALCHEMY_TRACK_MODIFICATIONS = False
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

REMEMBER_COOCKIE_DURATION = timedelta(days=1)
