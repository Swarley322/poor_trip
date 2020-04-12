from datetime import datetime, timedelta
from pytz import timezone
from webapp.trip.models import AvgPriceReviews


def get_cities_dict(money, checkin, checkout):
    # parsing_date = (datetime.now(timezone("Europe/Moscow")) - timedelta(days=1)).strftime("%d-%m-%Y")
    parsing_date = datetime.now(timezone("Europe/Moscow")).strftime("%d-%m-%Y")
    days = int((datetime.strptime(checkout, "%d/%m/%Y") -
                datetime.strptime(checkin, "%d/%m/%Y")).days)
    week_number = int(datetime.strptime(checkin, "%d/%m/%Y").strftime("%W"))
    cities = {
        "Europe": {
            "England": [],
            "Russia": [],
            "Germany": [],
            "Spain": [],
            "France": []
            },
        "Asia": {
            "Japan": [],
            "South Korea": [],
            "China": [],
            "Singapore": []
            },
        "America": {
            "USA": [],
            "Canada": []
            }
    }
    for city in AvgPriceReviews.query.filter(AvgPriceReviews.week_number == week_number) \
                                     .filter(AvgPriceReviews.parsing_date == parsing_date).all():
        if city.avg_day_price * days < money:
            result = {
                "name": city.city.ru_name,
                "price": city.avg_day_price * days,
                "checkin": checkin,
                "checkout": checkout,
                "money": money
            }
            cities[city.city.eng_part_of_the_world][city.city.eng_country].append(result)
    return cities



