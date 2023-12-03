bootstrap:
	rm -Rf testproject

	poetry run cookiecutter --no-input ./

build:
	docker build --build-arg POETRY_VERSION=1.6.1 --build-arg PYTHON_VERSION=3.11 --tag f213/django testproject
