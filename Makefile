# CURRENT_DIR = $(shell pwd)
all: t1 t3 t2
	@echo DONE	

t1:
	@export FLASK_APP=webapp && export FLASK_ENV=development && flask run

t2:
	@python3 get_hotels.py

t3:
	@redis-server

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