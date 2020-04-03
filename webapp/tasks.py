from celery import Celery
from webapp import create_app
from datetime import datetime, timedelta
from webapp.trip.get_all_hotels import get_all_hotels
from webapp.trip.models import City
from webapp.db import db

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
    with open("cities.txt", "r") as f:
        data = f.read().splitlines(True)
        if data:
            f.seek(0)
            city = f.readline().strip()
            checkin = f.readline().strip()
            checkout = f.readline().strip()
            get_all_hotels(city, checkin, checkout)
            print(f"{city} done")
            with open("cities.txt", "w") as f2:
                f2.writelines(data[3:])
        else:
            print("All cities has been parsed")


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



# @celery.task()
# def task1():
#     print("run task1")
