#!/bin/bash -e

cp src/app/.env.ci src/app/.env

docker compose down --volumes
docker compose up --detach

poetry install

poetry run python src/manage.py collectstatic
poetry run python src/manage.py startapp some_app
poetry run python src/manage.py makemigrations -n "initial"
poetry run python src/manage.py migrate

poetry run isort src/users/migrations/0001_initial.py

make lint test
