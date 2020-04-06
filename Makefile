all: flask worker tasker

flask:
	@flask run --host=0.0.0.0

worker:
	@celery -A webapp.tasks:celery worker --max-tasks-per-child=1 --concurrency=1 --time-limit=500 -B  --loglevel=info

.PHONY:all
