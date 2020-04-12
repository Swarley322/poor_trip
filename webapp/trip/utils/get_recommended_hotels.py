from datetime import datetime, timedelta
from sqlalchemy import or_
from pytz import timezone
from webapp.trip.models import AvgPriceReviews, City, Hotel


def get_best_hotels(city, checkin, checkout, money):
    # parsing_date = (datetime.now(timezone("Europe/Moscow")) - timedelta(days=1)).strftime("%d-%m-%Y")
    parsing_date = datetime.now(timezone("Europe/Moscow")).strftime("%d-%m-%Y")
    week_number = int(datetime.strptime(checkin, "%d/%m/%Y").strftime("%W"))
    year = int(datetime.strptime(checkin, "%d/%m/%Y").strftime("%Y"))
    city_id = City.query.filter(or_(
                            City.ru_name == city.title(),
                            City.eng_name == city.title()
                            )).first().id
    avg_reviews = AvgPriceReviews.query.filter(AvgPriceReviews.city_id == city_id) \
                                       .filter(AvgPriceReviews.parsing_date == parsing_date) \
                                       .filter(AvgPriceReviews.year == year) \
                                       .first().avg_reviews
    # avg_day_price = AvgPriceReviews.query.filter(AvgPriceReviews.city_id == city_id) \
    #                                      .filter(AvgPriceReviews.parsing_date == parsing_date) \
    #                                      .filter(AvgPriceReviews.year == year) \
    #                                      .first().avg_day_price
    result = []
    for hotel in Hotel.query.filter(Hotel.parsing_date == parsing_date) \
                            .filter(Hotel.week_number == week_number) \
                            .filter(Hotel.year == year) \
                            .filter(Hotel.city_id == city_id):
        if hotel.reviews and hotel.week_price and \
           hotel.week_price <= money and avg_reviews <= hotel.reviews:
            result.append({
                "hotel_name": hotel.name,
                "rating": hotel.rating,
                "stars": hotel.stars,
                "url": hotel.hotel_link,
                "price": hotel.week_price,
                "img": hotel.img_url
            })
        else:
            continue
    return sorted(result, key=lambda x: x['rating'], reverse=True)
