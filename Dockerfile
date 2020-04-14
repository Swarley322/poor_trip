FROM python:3.7

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt
RUN python fixtures/create_database_folder.py 
RUN export FLASK_APP=webapp && flask db upgrade
RUN python import_cities.py
RUN python import_attractions.py
RUN python import_aiports_id.py


ENTRYPOINT make -j