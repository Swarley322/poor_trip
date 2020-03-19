import os
from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_TASK_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
        "tasker": {
            "task": "webapp.tasks.get_hotels",
            "schedule": crontab(minute=10),
            "args": ()
        }
}
