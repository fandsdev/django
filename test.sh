#!/bin/bash

source venv/bin/activate

set -e

cd testing

rm -Rf django
echo |cookiecutter ../
