import os
import time
from celery import Celery
from celery.schedules import crontab
from datetime import datetime, timedelta

from webapp import create_app
from webapp.db import db
from webapp.parser.booking import get_all_hotels
from webapp.parser.live_prices import safe_city_prices
from webapp.trip.models import City

current_date = datetime.now()
app = create_app()
db.init_app(app)


CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
# CELERY_BROKER_URL = 'redis://localhost:6379/0'

celery = Celery('tasks', broker=CELERY_BROKER_URL)
# def make_celery(app):
#     celery = Celery(
#         app.import_name,
#         backend=app.config['CELERY_RESULT_BACKEND'],
#         broker=app.config['CELERY_BROKER_URL']
#         )
#     celery.conf.update(app.config)

#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)

#     celery.Task = ContextTask
#     return celery


# celery = make_celery(app)


@celery.task()
def get_hotels():
    with app.app_context():
        with open("cities.txt", "r") as f:
            data = f.read().splitlines(True)
            if data:
                f.seek(0)
                city = f.readline().strip()
                checkin = f.readline().strip()
                checkout = f.readline().strip()
                try:
                    get_all_hotels(city, checkin, checkout)
                    print(f"{city} - {checkin} - {checkout} completed")
                    with open("cities.txt", "w") as f2:
                        f2.writelines(data[3:])
                except:
                    return "Parsing crashed"
            else:
                return "All cities has been parsed"


@celery.task()
def create_city_list():
    with app.app_context():
        cities = [x.ru_name for x in City.query.all()]
        with open("cities.txt", "w") as f:
            for city in cities:
                checkin = current_date + timedelta(days=1)
                for _ in range(5):
                    checkout = checkin + timedelta(days=7)
                    f.write(city + "\n")
                    f.write(checkin.strftime("%d/%m/%Y") + "\n")
                    f.write(checkout.strftime("%d/%m/%Y") + "\n")
                    checkin = checkout


@celery.task()
def get_live_prices():
    for city in City.query.all():
        with app.app_context():
            safe_city_prices(city.eng_name)
        time.sleep(5)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/1'), get_hotels.s())
    sender.add_periodic_task(crontab(minute=0, hours=0), create_city_list.s())
    sender.add_periodic_task(crontab(minute=0, hours=1), get_live_prices.s())


# @celery.task()
# def task1():
#     print("run task1")
