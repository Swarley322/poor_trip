FROM python:3.7

COPY . .
RUN pip install -r requirements.txt
RUN python create_db.py
RUN python city_list.py

ENTRYPOINT make -j