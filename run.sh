#!/bin/sh -ex
celery -A webapp.tasks:celery worker --loglevel=info
celery -A webapp.tasks.celery beat