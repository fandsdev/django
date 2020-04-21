#!/bin/bash -e

echo -ne "Running with "

python --version

echo Creating and populating virtualenv..

python -m venv venv
. venv/bin/activate

pip install --upgrade pip
pip install pip-tools

./update-deps.sh

cd src

echo Collecting static assets...
./manage.py collectstatic

echo Running initial migrations...
./manage.py migrate

echo Running flake8..
flake8

echo Running pytest...
pytest -x

echo Done
