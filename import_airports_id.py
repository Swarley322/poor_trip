import csv
from webapp import create_app
from webapp import db
from webapp.trip.models import Airport_Ids

app = create_app()

with app.app_context():
    with open('fixtures/airport_ids.csv', 'r', encoding='utf-8', newline='') as f:
        fields = ['name', 'id']
        cities = csv.DictReader(f, fields, delimiter=';')
        for city in cities:
            id_exists = db.session.query(db.exists().where(Airport_Ids.city == city['name'])).scalar()
            if not id_exists:
                new_id = Airport_Ids(
                    city=city['name'].lower().strip(),
                    airport_id=city['id'].strip()
                )
                db.session.add(new_id)
                db.session.commit()
            else:
                continue
