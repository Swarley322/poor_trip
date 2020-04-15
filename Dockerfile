FROM python:3.7

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt
RUN chmod +x import.sh
# RUN export FLASK_APP=webapp && flask db upgrade
# RUN python import_cities.py
# RUN python import_attractions.py
# RUN python import_airports_id.py


# ENTRYPOINT ["flask", "run"]
ENTRYPOINT ./import.sh
# ENTRYPOINT make -j

# ENTRYPOINT ["./import.sh"]
# CMD ["flask", "run"]