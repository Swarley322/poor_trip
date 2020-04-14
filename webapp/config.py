import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

# CHROMEDRIVER = os.path.join(basedir.replace('/webapp', ""), 'chromedriver')

DATA_PATH = "database"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', DATA_PATH, 'webapp.db')
# SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

REMEMBER_COOCKIE_DURATION = timedelta(days=7)

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
# CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
# CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
