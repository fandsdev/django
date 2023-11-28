VENV = cd testproject && poetry run python src/manage.py

test: bootstrap
	$(VENV) makemigrations --check
	$(VENV) startapp test_app

bootstrap:
	rm -Rf testproject

	cookiecutter --no-input ./

coverage:
	$(VENV) -m pip install pytest-cov
	$(VENV) -m pytest --cov-report=xml --cov=core --cov=users --cov=a12n --cov=sepulkas
