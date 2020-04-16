import csv

from webapp import create_app
from webapp.db import db
from webapp.trip.models import City

app = create_app()

with app.app_context():
    with open('fixtures/cities_list.csv', 'r', encoding='utf-8-sig', newline='') as f:
        fields = ['eng_name', 'eng_country', 'eng_part_of_the_world', 'ru_name', 'ru_country', "ru_part_of_the_world"]
        cities = csv.DictReader(f, fields, delimiter=';')
        for city in cities:
            city_exist = db.session.query(db.exists().where(City.eng_name == city['eng_name'].lower().strip())).scalar()
            if not city_exist:
                city = City(
                    eng_name=city["eng_name"].lower(),
                    eng_country=city["eng_country"].lower(),
                    eng_part_of_the_world=city["eng_part_of_the_world"].lower(),
                    ru_name=city["ru_name"].lower(),
                    ru_country=city["ru_country"].lower(),
                    ru_part_of_the_world=city["ru_part_of_the_world"].lower()
                )
                db.session.add(city)
                db.session.commit()
            else:
                continue
