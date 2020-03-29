# CURRENT_DIR = $(shell pwd)
all: flask worker tasker
	@echo DONE	

flask:
	@export FLASK_APP=webapp && export FLASK_ENV=development && FLASK_APP_PORT=5000 && flask run --host=0.0.0.0
worker:
	@celery -A webapp.tasks:celery worker --pidfile= --loglevel=info

tasker:
	@celery -A webapp.tasks.celery beat

.PHONY:all

# # .PHONY: default test
# .PHONY: all
# all: t5 t4 t1
# 	@echo Making $@

# t1: t3 t2
# 	touch $@

# t2:
# 	cp t3 $@

# t3:
# 	touch $@

# t4:
# 	touch $@

# t5:
# 	touch $@