SIMULTANEOUS_TEST_JOBS = 4

manage = uv run python src/manage.py

fmt:
	uv run ruff check src --fix --unsafe-fixes
	uv run ruff format src
	uv run toml-sort pyproject.toml

lint:
	$(manage) check
	$(manage) makemigrations --check --dry-run --no-input

	uv run ruff check src
	uv run ruff format --check src
	uv run mypy src
	uv run toml-sort --check pyproject.toml
	uv run pymarkdown scan README.md
	uv run dotenv-linter src/app/.env.ci

test:
	uv run pytest --dead-fixtures
	uv run pytest --create-db --exitfirst --numprocesses ${SIMULTANEOUS_TEST_JOBS}
