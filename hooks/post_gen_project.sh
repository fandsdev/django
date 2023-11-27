#!/bin/bash -e

cp src/core/.env.ci src/core/.env

poetry install

poetry run python src/manage.py collectstatic
poetry run python src/manage.py migrate

make fmt lint test
