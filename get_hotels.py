from webapp import create_app
from webapp.get_all_hotels import get_all_hotels
from datetime import datetime, timedelta
from webapp.model import db, Hotel, AvgPriceReviews, City

current_date = datetime.now()
app = create_app()
with app.app_context():
    for city in City.query.all():
        checkin = current_date
        for _ in range(5):
            checkout = checkin + timedelta(days=7)
            get_all_hotels(city.ru_name,
                           checkin.strftime("%d/%m/%Y"),
                           checkout.strftime("%d/%m/%Y"))
            checkin = checkout
