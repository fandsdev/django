#!/bin/bash -e

cp src/app/.env.ci src/app/.env

poetry install

poetry run python src/manage.py collectstatic
poetry run python src/manage.py startapp some_app
poetry run python src/manage.py makemigrations -n "initial"

poetry run isort src/users/migrations/0001_initial.py

poetry run python src/manage.py migrate

make fmt lint test
