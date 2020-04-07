all: flask worker tasker

flask:
	@flask run --host=0.0.0.0

worker:
	@celery -A webapp.tasks:celery worker --max-tasks-per-child=1 --concurrency=2 --time-limit=350 -B --loglevel=info 
  

.PHONY:all
