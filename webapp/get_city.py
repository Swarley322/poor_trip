from datetime import datetime
from webapp.model import AvgPriceReviews


def get_city_dict(money, checkin, checkout):
    days = int((datetime.strptime(checkout, "%d/%m/%Y") -
                datetime.strptime(checkin, "%d/%m/%Y")).days)
    week_number = int(datetime.strptime(checkin, "%d/%m/%Y").strftime("%W"))
    citys = []
    for city in AvgPriceReviews.query.filter(AvgPriceReviews.week_number == week_number).all():
        if city.avg_day_price * days < money:
            result = {
                "name": city.city.ru_name,
                "price": city.avg_day_price * days,
                "checkin": checkin,
                "checkout": checkout,
                "money": money
            }
            citys.append(result)
    return citys
