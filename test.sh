#!/bin/bash

source venv/bin/activate

set -e

mkdir -p testing
cd testing

rm -Rf django
echo |cookiecutter ../
