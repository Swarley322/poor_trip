FROM python:3.7

COPY . .
RUN pip install -r requirements.txt
RUN export FLASK_APP=webapp && flask db upgrade
RUN python import_cities.py
RUN python import_attractions.py
RUN python import_aiports_id.py

ENTRYPOINT make -j