FROM python:3.7 as webapp

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=ru_RU.UTF-8

ENV LANG ru_RU.UTF-8 
# ENTRYPOINT flask run --host=0.0.0.0
# CMD ["uwsgi", "app.ini"]
CMD ["python", "run.py"]


FROM poor_trip_webapp as celery
# RUN locale-gen ru_RU.UTF-8
# ENV LANGUAGE ru_RU:ru
# ENV LANG ru_RU.UTF-8
# ENV LC_ALL ru_RU.UTF-8
# ENV LC_TIME=ru_RU.UTF-8
# RUN locale-gen ru_RU.UTF-8 && dpkg-reconfigure locales

ENTRYPOINT make
