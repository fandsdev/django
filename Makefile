bootstrap:
	rm -rf testproject

	poetry run cookiecutter --no-input ./

fmt:
	poetry run toml-sort pyproject.toml

lint:
	poetry run toml-sort pyproject.toml --check
	poetry run pymarkdown scan README.md
