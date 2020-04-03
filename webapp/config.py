import os
from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')
# SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# CELERY_BROKER_URL = 'redis://localhost:6379'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
# SCHEDULE = os.environ.get("SCHEDULE")

CELERY_TASK_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
        "parsing": {
            "task": "webapp.tasks.get_hotels",
            "schedule": crontab(minute="*/8"),
            "args": ()
        },
        "create_city_list": {
            "task": "webapp.tasks.create_city_list",
            "schedule": crontab(minute=0, hour="*/4"),
            "args": ()
        }
}
# CELERYBEAT_SCHEDULE = {
#         "tasker": {
#             "task": "webapp.tasks.task1",
#             "schedule": 5.0,
#             "args": ()
#         }
# }
