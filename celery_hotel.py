from webapp import create_app
from webapp.get_all_hotels import get_all_hotels
from datetime import datetime, timedelta
from webapp.model import db, Hotel, AvgPriceReviews, City

# from celery import Celery
# from celery.schedules import crontab

current_date = datetime.now()
app = create_app()

# app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
# celery = Celery('hotel', broker="redis://localhost:6360/0")

# @celery.task
def hotel():
# with app.app_context():
#     for city in City.query.all():
#         checkin = current_date + timedelta(days=1)
#         for _ in range(2):
#             checkout = checkin + timedelta(days=7)
#             get_all_hotels(city.ru_name,
#                             checkin.strftime("%d/%m/%Y"),
#                             checkout.strftime("%d/%m/%Y"))
#             checkin = checkout
        # city = "Нью-Йорк"
        # checkin = current_date + timedelta(days=1)
        # for _ in range(5):
        #     checkout = checkin + timedelta(days=7)
        #     get_all_hotels(city,
        #                    checkin.strftime("%d/%m/%Y"),
        #                    checkout.strftime("%d/%m/%Y"))
        #     checkin = checkout
        
        # celery.conf.beat_schedule = {
        #     "hotel-parsing": {
        #                 "task": "hotel.hotel",
        #                 "args": (1, 2),
        #                 "schedule": crontab(minute=10)
        #                 }
        # }
