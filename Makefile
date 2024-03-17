remove-prev-generated-project-if-exists:
	if [ -d "testproject" ]; then \
		cd testproject && docker compose down --volumes; \
		cd .. && rm -Rf testproject; \
	fi

bootstrap: remove-prev-generated-project-if-exists
	poetry run cookiecutter --no-input ./

fmt:
	poetry run toml-sort pyproject.toml

lint:
	poetry run toml-sort pyproject.toml --check
	poetry run pymarkdown scan README.md
