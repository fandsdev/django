SIMULTANEOS_TEST_JOBS = 4

manage = poetry run python src/manage.py

fmt:
	poetry run ruff check src --fix --unsafe-fixes
	poetry run ruff format src
	poetry run toml-sort pyproject.toml

lint:
	$(manage) check
	$(manage) makemigrations --check --dry-run --no-input

	poetry run ruff check src
	poetry run ruff format --check src
	poetry run mypy src
	poetry run toml-sort pyproject.toml --check
	poetry run pymarkdown scan README.md
	poetry run dotenv-linter src/app/.env.ci

test:
	poetry run pytest --dead-fixtures
	poetry run pytest --create-db --exitfirst --numprocesses ${SIMULTANEOS_TEST_JOBS}
