NUMPROCESSES = 4

manage = poetry run python src/manage.py

checks:
	$(manage) check
	$(manage) makemigrations --check --dry-run --no-input

	poetry run isort --check-only src tests
	poetry run black --check src tests
	poetry run flake8 src tests
	poetry run mypy src tests
	poetry run toml-sort pyproject.toml --check
	poetry run pymarkdown scan README.md
	poetry run dotenv-linter src/core/.env.ci

fmt:
	poetry run autoflake --in-place --remove-all-unused-imports --recursive src tests
	poetry run isort src tests
	poetry run black src tests
	poetry run toml-sort pyproject.toml

test:
	poetry run pytest --dead-fixtures
	poetry run pytest --create-db --exitfirst --numprocesses ${NUMPROCESSES}
