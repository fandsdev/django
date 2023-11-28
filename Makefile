test: bootstrap
	cd testproject && poetry run src/manage.py makemigrations --check
	cd testproject && poetry run src/manage.py startapp test_app

	make coverage

bootstrap:
	rm -Rf testproject

	poetry run cookiecutter --no-input ./

	cd testproject && poetry install

coverage:
	cd testproject && poetry run python -m pytest --cov-report=xml --cov=core --cov=apps.a12n --cov=apps.users --cov=sepulkas
