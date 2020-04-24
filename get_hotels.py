from webapp import create_app
from webapp.parser.booking import get_all_hotels
from datetime import datetime, timedelta
from webapp.db import db
from webapp.trip.models import City

current_date = datetime.now()
july = datetime.strptime("01/07/2020", "%d/%m/%Y")

app = create_app()
db.init_app(app)

with app.app_context():
    for city in City.query.all():
        if current_date < july:
            checkin = july
        else:
            checkin = current_date + timedelta(days=1)
        for _ in range(2):
            start = datetime.now()
            checkout = checkin + timedelta(days=7)
            get_all_hotels(city.ru_name,
                           checkin.strftime("%d/%m/%Y"),
                           checkout.strftime("%d/%m/%Y"))
            checkin = checkout
            end = datetime.now()
            print(f"{city.ru_name} done for {end - start}")
