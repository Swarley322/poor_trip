FROM python:3.7 as webapp

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

ENTRYPOINT flask run --host=0.0.0.0


FROM poor_trip_webapp as celery

ENTRYPOINT make
