VENV=cd testing/django/src && ../venv/bin/python

test: bootstrap
	$(VENV) ./manage.py makemigrations --check
	$(VENV) ./manage.py startapp test_app

bootstrap:
	rm -Rf testing
	mkdir -p testing
	cd testing && cookiecutter --no-input ../

coverage:
	$(VENV) -m pip install pytest-cov
	$(VENV) -m pytest --cov-report=xml --cov=app --cov=users --cov=a12n --cov=sepulkas
