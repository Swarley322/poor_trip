FROM python:3.7

COPY . .
RUN pip install -r requirements.txt
RUN python create_db.py
RUN python city_list.py

ENV FLASK_APP webapp
ENV FLASK_ENV development
ENV FLASK_APP_PORT 5000

ENTRYPOINT make -j