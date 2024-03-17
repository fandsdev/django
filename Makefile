setup-dev-environment:
	cp {{\ cookiecutter.name\ }}/docker-compose.yml ./

	docker-compose down --volumes
	docker-compose up --detach

	rm -rf testproject

bootstrap: setup-dev-environment
	poetry run cookiecutter --no-input ./

	rm docker-compose.yml

fmt:
	poetry run toml-sort pyproject.toml

lint:
	poetry run toml-sort pyproject.toml --check
	poetry run pymarkdown scan README.md
