FROM python:3.7
# RUN apt-get update
# RUN apt-get install python3.7 -y
# RUN apt-get -y install python3-pip


COPY . .
RUN pip install -r requirements.txt
RUN python create_db.py
RUN python city_list.py


# EXPOSE 5000

# ENTRYPOINT export FLASK_APP=webapp && export FLASK_ENV=development && FLASK_APP_PORT=5000 && flask run --host=0.0.0.0
# ENTRYPOINT [ "/bin/sh" ]
ENTRYPOINT make -j