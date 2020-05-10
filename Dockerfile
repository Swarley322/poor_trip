FROM python:3.7 as webapp

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=ru_RU.UTF-8

ENV LANG ru_RU.UTF-8 
ENTRYPOINT uwsgi --http-socket :5000 --module wsgi:app --master --processes 4 --threads 2


FROM poor_trip_webapp as celery

ENTRYPOINT make
