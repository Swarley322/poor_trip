import random
from webapp.trip.models import Attraction, City


def get_attractions_list(city):
    city_id = City.query.filter(City.ru_name == city.lower()).first().id
    attractions = Attraction.query.filter(Attraction.city_id == city_id)
    result = []
    for attraction in attractions:
        result.append({
            "name": attraction.name,
            "img_url": attraction.img_url,
            "address": attraction.address,
            "description": attraction.description,
            "url": attraction.link
        })
    random.shuffle(result)
    return result
