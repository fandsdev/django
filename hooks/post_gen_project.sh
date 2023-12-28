#!/bin/bash -e

cp src/core/.env.ci src/core/.env

docker compose up --detach

poetry install

poetry run python src/manage.py collectstatic
poetry run python src/manage.py startapp some_app
poetry run python src/manage.py migrate

make lint test
