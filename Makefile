bootstrap:
	rm -Rf testproject

	poetry run cookiecutter --no-input ./

build:
	docker build --build-arg PYTHON_VERSION=3.11 --tag f213/django testproject

fmt:
	poetry run toml-sort pyproject.toml

lint:
	poetry run toml-sort pyproject.toml --check
	poetry run pymarkdown scan README.md
