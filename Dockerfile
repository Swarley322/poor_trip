FROM python:3.7

COPY . .
RUN pip install -r requirements.txt
RUN export FLASK_APP=webapp && flask db upgrade
RUN python3 city_list.py

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

ENTRYPOINT make -j