SIMULTANEOUS_TEST_JOBS = 4

.DEFAULT_GOAL := help

install-dev-deps:
	uv sync --locked

install-deps:
	uv sync --locked --no-dev

fmt:
	uv run ruff check src --fix --unsafe-fixes
	uv run ruff format src
	uv run toml-sort pyproject.toml

lint:
	uv run python src/manage.py check
	uv run python src/manage.py makemigrations --check --dry-run --no-input
	uv run python src/manage.py spectacular --api-version v1 --fail-on-warn > /dev/null
	uv run ruff check src
	uv run ruff format --check src
	uv run mypy src
	uv run toml-sort --check pyproject.toml
	uv run pymarkdown scan README.md
	uv run dotenv-linter src/app/.env.ci

test:
	uv run pytest --dead-fixtures
	uv run pytest --create-db --exitfirst --numprocesses ${SIMULTANEOUS_TEST_JOBS}

help:
	@echo "Makefile for {{ cookiecutter.name }}"
	@echo ""
	@echo "Usage:"
	@echo "  make install-dev-deps   Install development dependencies"
	@echo "  make install-deps       Install production dependencies"
	@echo "  make fmt                Format code"
	@echo "  make lint               Lint code"
	@echo "  make test               Run tests"
	@echo "  make help               Show this help message"
