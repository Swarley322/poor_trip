import os
from celery import Celery
from celery.schedules import crontab

from webapp import create_app
from webapp.db import db
from webapp.task_funcs.tasks import get_hotels_task, create_city_list_task, get_live_prices_task, clear_cities_txt_task

app = create_app()
db.init_app(app)


CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
# CELERY_BROKER_URL = 'redis://localhost:6379/0'

celery = Celery('tasks', broker=CELERY_BROKER_URL)


@celery.task(time_limit=359)
def get_hotels():
    with app.app_context():
        print(get_hotels_task())


@celery.task()
def create_city_list():
    with app.app_context():
        print(create_city_list_task())


@celery.task()
def get_live_prices():
    with app.app_context():
        print(get_live_prices_task())


@celery.task()
def clear_cities_txt():
    print(clear_cities_txt_task())


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute="*/5"), get_hotels.s())
    sender.add_periodic_task(crontab(minute=57, hour=20), clear_cities_txt.s())
    sender.add_periodic_task(crontab(minute=0, hour=21), create_city_list.s())
    sender.add_periodic_task(crontab(minute=5, hour=21), get_live_prices.s())


# @celery.task()
# def task1():
#     print("run task1")
