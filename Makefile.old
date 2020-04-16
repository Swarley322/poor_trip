all: flask worker

flask:
	@flask run --host=0.0.0.0

worker:
	@celery -A webapp.tasks:celery worker --max-tasks-per-child=1 --concurrency=1 -B --loglevel=info 

.PHONY:all
