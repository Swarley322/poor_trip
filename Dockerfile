FROM python:3.7

COPY . /test
RUN pip install -r /test/requirements.txt

EXPOSE 5000

ENTRYPOINT export FLASK_APP=webapp && export FLASK_ENV=development && flask run