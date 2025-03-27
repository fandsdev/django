#!/bin/bash -e

cp src/app/.env.ci src/app/.env

poetry lock --no-update
poetry install

poetry run python src/manage.py collectstatic
poetry run python src/manage.py makemigrations -n "initial"
poetry run python src/manage.py migrate

make lint
make test
