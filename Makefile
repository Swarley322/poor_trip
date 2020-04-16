.PHONY: all migrations

all: delay migrations import tasks

delay:
	@echo wait 20 sec
	@sleep 20

migrations:
	@flask db upgrade
	@echo flask upgraded

import:
	@python import_cities.py
	@python import_attractions.py
	@python import_airports_id.py
	@echo imported

tasks:
	@echo running celery
	@celery -A webapp.tasks:celery worker --max-tasks-per-child=1 --concurrency=1 -B --loglevel=info
	