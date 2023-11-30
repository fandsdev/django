#!/bin/bash -e

cp src/core/.env.ci src/core/.env

poetry install

poetry run python src/manage.py collectstatic
poetry run python src/manage.py migrate
poetry run python src/manage.py startapp some_app --entity_name some_entity

make checks test
