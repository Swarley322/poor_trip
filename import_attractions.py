import csv
import sys

from webapp import create_app
from webapp.db import db
from webapp.trip.models import Attractions, City

app = create_app()
csv.field_size_limit(sys.maxsize)

with app.app_context():
    with open('fixtures/attractions.csv', 'r', encoding='utf-8', newline='') as f:
        fields = ['city', 'name', 'address', 'description', 'img_url', "link"]
        attractions = csv.DictReader(f, fields, delimiter=';')
        for attraction in attractions:
            city_id = City.query.filter(City.ru_name == attraction['city'].title()).first()
            attraction_exist = db.session.query(db.exists().where(Attractions.name == attraction['name'])).scalar()
            
            if not attraction_exist:
                new_attraction = Attractions(
                            city_id=city_id.id,
                            name=attraction['name'],
                            address=attraction['address'],
                            description=attraction['description'],
                            img_url=attraction['img_url'],
                            link=attraction['link'])
                db.session.add(new_attraction)
                db.session.commit()
