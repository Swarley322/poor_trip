import json

from webapp import create_app
from webapp.db import db
from webapp.trip.models import City

app = create_app()

with app.app_context():
    cities = [city.eng_name for city in City.query.all()]
    for city in cities:
        with open(f'fixtures/living_prices/{city}.json') as f:    
            data = json.load(f)
            update = City.query.filter_by(eng_name=city.lower()).first()
            update.living_prices = data
            db.session.commit()
