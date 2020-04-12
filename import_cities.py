import csv

from webapp import create_app
from webapp.db import db
from webapp.trip.models import City

app = create_app()

with app.app_context():
    with open('fixtures/cities_list.csv', 'r', encoding='utf-8', newline='') as f:
        fields = ['eng_name', 'eng_country', 'eng_part_of_the_world', 'ru_name', 'ru_country', "ru_part_of_the_world"]
        cities = csv.DictReader(f, fields, delimiter=';')
        for city in cities:
            city = City(
                eng_name=city["eng_name"],
                eng_country=city["eng_country"],
                eng_part_of_the_world=city["eng_part_of_the_world"],
                ru_name=city["ru_name"],
                ru_country=city["ru_country"],
                ru_part_of_the_world=city["ru_part_of_the_world"]
            )
            db.session.add(city)
            db.session.commit()
