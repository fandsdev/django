#!/bin/bash -e


echo Running pip-compile...

for dep in 'requirements.in' 'dev-requirements.in';
do
    pip-compile -q --generate-hashes $dep
done

echo Done

echo Installing local deps

pip-sync requirements.txt dev-requirements.txt
