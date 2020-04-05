all: flask worker tasker

flask:
	@flask run --host=0.0.0.0

worker:
	@celery -A webapp.tasks:celery worker --pidfile= -B --maxtaskperchild=1 --loglevel=info

.PHONY:all
