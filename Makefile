VENV=cd testproject/django/src && ../venv/bin/python

test: bootstrap
	$(VENV) ./manage.py makemigrations --check
	$(VENV) ./manage.py startapp test_app

bootstrap:
	rm -Rf testproject
	mkdir -p testproject
	cd testproject && cookiecutter --no-input ../

coverage:
	$(VENV) -m pip install pytest-cov
	$(VENV) -m pytest --cov-report=xml --cov=app --cov=users --cov=a12n --cov=sepulkas
