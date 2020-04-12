import random
from webapp.trip.models import Attractions, City


def get_attractions_list(city):
    city_id = City.query.filter(City.ru_name == city.title()).first().id
    attractions = Attractions.query.filter(Attractions.city_id == city_id)
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
