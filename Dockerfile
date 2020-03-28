FROM python:3.7

COPY . .
RUN pip install -r requirements.txt

# EXPOSE 5000

# ENTRYPOINT export FLASK_APP=webapp && export FLASK_ENV=development && FLASK_APP_PORT=5000 && flask run --host=0.0.0.0
ENTRYPOINT [ "/bin/sh" ]
CMD ["./run.sh"]