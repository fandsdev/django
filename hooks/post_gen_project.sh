#!/bin/bash -e

echo -ne "Running with "

python --version

echo Creating and populating virtualenv..

python -m venv venv
. venv/bin/activate

pip install --upgrade pip
pip install pip-tools
pip-sync requirements.txt dev-requirements.txt

cd src && ./manage.py migrate

echo Done
