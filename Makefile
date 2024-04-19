bootstrap:
	rm -rf testproject

	cookiecutter --no-input --keep-project-on-failure ./

fmt:
	poetry run toml-sort pyproject.toml

lint:
	poetry run toml-sort pyproject.toml --check
	poetry run pymarkdown scan README.md
