#!/bin/bash -e

cp src/core/.env.ci src/core/.env

poetry install

poetry run python src/manage.py collectstatic
poetry run python src/manage.py startapp some_app --entity_name some_entity
poetry run python src/manage.py makemigrations --name some_entity
poetry run python src/manage.py migrate

make checks test
