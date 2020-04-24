import re

from datetime import datetime, timedelta
from sqlalchemy import or_
from pytz import timezone
from webapp.trip.models import AvgPriceReviews, City, Hotel


def get_best_hotels(city, checkin, checkout, money):
    # parsing_date = datetime.now(timezone("Europe/Moscow")).strftime("%d/%m/%Y")
    parsing_date = (datetime.now(timezone("Europe/Moscow")) - timedelta(days=2)).strftime("%d/%m/%Y")
    week_number = int(datetime.strptime(checkin, "%d/%m/%Y").strftime("%W"))
    year = int(datetime.strptime(checkin, "%d/%m/%Y").strftime("%Y"))

    days_staying = int(abs((datetime.strptime(checkin, "%d/%m/%Y") - datetime.strptime(checkout, "%d/%m/%Y")).days))
    real_checkin = "checkin=" + datetime.strptime(checkin, "%d/%m/%Y").strftime("%Y-%m-%d")
    real_checkout = "checkout=" + datetime.strptime(checkout, "%d/%m/%Y").strftime("%Y-%m-%d")
    city_id = City.query.filter(or_(
                            City.ru_name == city.lower(),
                            City.eng_name == city.lower()
                            )).first().id

    avg_reviews = AvgPriceReviews.query.filter_by(city_id=city_id) \
                                       .filter_by(parsing_date=parsing_date) \
                                       .filter_by(week_number=week_number) \
                                       .filter_by(year=year).first().avg_reviews
    result = []
    for hotel in Hotel.query.filter(Hotel.parsing_date == parsing_date) \
                            .filter(Hotel.week_number == week_number) \
                            .filter(Hotel.year == year) \
                            .filter(Hotel.city_id == city_id):
        if hotel.reviews and hotel.avg_day_price and \
                             hotel.avg_day_price * days_staying <= money and \
                             avg_reviews <= hotel.reviews:
            hotel_link = re.sub("checkin=\\d{4}-\\d{2}-\\d{2}", real_checkin, hotel.hotel_link)
            hotel_link = re.sub("checkout=\\d{4}-\\d{2}-\\d{2}", real_checkout, hotel_link)
            result.append({
                    "hotel_name": hotel.name,
                    "rating": hotel.rating,
                    "stars": hotel.stars,
                    "url": hotel_link,
                    "price": hotel.avg_day_price * days_staying,
                    "img": hotel.img_url,
                    "reviews": hotel.reviews
            })
        else:
            continue
    return sorted(result, key=lambda x: x['rating'], reverse=True)
