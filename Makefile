all: flask worker tasker

flask:
	@flask run --host=0.0.0.0
	# @export FLASK_APP=webapp && export FLASK_ENV=development && FLASK_APP_PORT=5000 && flask run

worker:
	@celery -A webapp.tasks:celery worker --pidfile= -B --loglevel=info

# tasker:
# 	@celery -A webapp.tasks.celery beat

.PHONY:all
