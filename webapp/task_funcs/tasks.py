import time

from pytz import timezone
from datetime import datetime, timedelta
from webapp.trip.models import City
from webapp.parser.live_prices import safe_city_prices
from webapp.parser.booking import get_all_hotels


current_date = datetime.now(timezone("Europe/Moscow"))


def get_hotels_task():
    with open("cities.txt", "r") as f:
        data = f.read().splitlines(True)
        if data:
            f.seek(0)
            city = f.readline().strip()
            checkin = f.readline().strip()
            checkout = f.readline().strip()
            hotels = get_all_hotels(city, checkin, checkout)
            if hotels:
                with open("cities.txt", "w") as f2:
                    f2.writelines(data[3:])
                return f"{city} - {checkin} - {checkout} completed"
            else:
                return f"{hotels}Parsing {city} - {checkin} - {checkout} crashed"

        else:
            return "All cities has been parsed"


def create_city_list_task():
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
    return f"Cities.txt - {current_date} created"


def get_live_prices_task():
    for city in City.query.all():
        safe_city_prices(city.eng_name)
        time.sleep(5)
    return f"Live prices - {current_date} parsed"
