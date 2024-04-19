bootstrap:
	rm -rf testproject

	cookiecutter --no-input --keep-project-on-failure ./

fmt:
	toml-sort pyproject.toml

lint:
	toml-sort pyproject.toml --check
	pymarkdown scan README.md
