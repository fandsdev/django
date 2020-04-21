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

./manage.py collectstatic
./manage.py migrate
pytest -x

echo Done
