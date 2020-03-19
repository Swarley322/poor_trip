from celery import Celery
from flask import Flask
from webapp import create_app
from webapp.get_all_hotels import get_all_hotels
from datetime import datetime, timedelta

current_date = datetime.now()
app = create_app()


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
        )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery_app = Flask(__name__)
celery_app.config.from_pyfile('config.py')
celery = make_celery(celery_app)


@celery.task()
def add(a, b):
    return a + b


@celery.task()
def get_hotels():
    with app.app_context():
        city = "Нью-Йорк"
        checkin = current_date + timedelta(days=1)
        for _ in range(5):
            checkout = checkin + timedelta(days=7)
            get_all_hotels(city,
                           checkin.strftime("%d/%m/%Y"),
                           checkout.strftime("%d/%m/%Y"))
            checkin = checkout
    print('get_hotels() executed')
