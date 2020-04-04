from datetime import datetime
from webapp.trip.models import AvgPriceReviews

current_day = datetime.now().strftime("%Y-%m-%d")


def get_city_dict(money, checkin, checkout):
    # days = int((checkout - checkin).days)
    # week_number = int(checkin.strftime("%W"))
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
            "South korea": [],
            "China": [],
            "Singapore": []
            },
        "America": {
            "USA": [],
            "Canada": []
            }
    }
    for city in AvgPriceReviews.query.filter(AvgPriceReviews.week_number == week_number) \
                                     .filter(AvgPriceReviews.parsing_date == current_day).all():
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

