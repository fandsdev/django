#!/bin/bash -e

cp src/app/.env.ci src/app/.env

uv sync --frozen

uv run python src/manage.py collectstatic
uv run python src/manage.py makemigrations --name "initial"
uv run python src/manage.py migrate

make lint
make test
