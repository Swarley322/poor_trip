#!/bin/sh

# export FLASK_APP=webapp && flask db upgrade
flask db upgrade

python import_cities.py
python import_attractions.py
python import_airports_id.py

flask run --host=0.0.0.0