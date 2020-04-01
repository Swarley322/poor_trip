FROM python:3.7

COPY . .
RUN pip install -r requirements.txt
RUN export FLASK_APP=webapp && flask db upgrade
RUN python city_list.py

ENTRYPOINT make -j