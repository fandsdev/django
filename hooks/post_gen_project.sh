#!/bin/bash -e

rm -rf .mypy_cache \
   .pytest_cache \
   .venv

cp src/core/.env.ci src/core/.env

poetry install

poetry run python src/manage.py collectstatic
poetry run python src/manage.py migrate
poetry run python src/manage.py startapp test_app

make lint test
