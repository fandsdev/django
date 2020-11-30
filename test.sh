#!/bin/bash

source venv/bin/activate

set -e

mkdir -p testing
cd testing

rm -Rf django
cookiecutter --no-input ../

# Smoke-testing custom ./manage.py commands

source django/venv/bin/activate
cd django/src

./manage.py startapp test_app
./manage.py makemigrations -n testappmigration01
