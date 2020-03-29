from celery import Celery
from flask import Flask
from webapp import create_app
from webapp.get_all_hotels import get_all_hotels
from datetime import datetime, timedelta
from webapp.model import db, City

current_date = datetime.now()
app = create_app()
db.init_app(app)


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


celery = make_celery(app)


@celery.task()
def get_hotels():
    for city in City.query.all():
        checkin = current_date + timedelta(days=1)
        for _ in range(1):
            checkout = checkin + timedelta(days=7)
            get_all_hotels(city.ru_name,
                           checkin.strftime("%d/%m/%Y"),
                           checkout.strftime("%d/%m/%Y"))
            checkin = checkout
    # city = "Нью-Йорк"
    # checkin = current_date + timedelta(days=1)
    # for _ in range(2):
    #     checkout = checkin + timedelta(days=7)
    #     get_all_hotels(city,
    #                     checkin.strftime("%d/%m/%Y"),
    #                     checkout.strftime("%d/%m/%Y"))
    #     checkin = checkout
    #     print(f"{city} done")


# @celery.task()
# def task1():
#     print("run task1")


# @celery.task()
# def task2():
#     print("run task2")


