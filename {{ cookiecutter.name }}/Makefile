SIMULTANEOS_TEST_JOBS = 4

manage = poetry run python src/manage.py

fmt:
	poetry run autoflake --in-place --remove-all-unused-imports --recursive src
	poetry run isort src
	poetry run black src
	poetry run toml-sort pyproject.toml

lint:
	$(manage) check
	$(manage) makemigrations --check --dry-run --no-input

	poetry run isort --check-only src
	poetry run black --check src
	poetry run flake8 src
	poetry run mypy src
	poetry run toml-sort pyproject.toml --check
	poetry run pymarkdown scan README.md
	poetry run dotenv-linter src/app/.env.ci

test:
	poetry run pytest --dead-fixtures
	poetry run pytest --create-db --exitfirst --numprocesses ${SIMULTANEOS_TEST_JOBS}
