VENV=cd testing/django/src && ../venv/bin/python

test: bootstrap
	$(VENV) ./manage.py makemigrations --check
	$(VENV) ./manage.py startapp test_app

bootstrap:
	rm -Rf testing
	mkdir -p testing
	cd testing && cookiecutter --no-input ../
