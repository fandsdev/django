SIMULTANEOUS_TEST_JOBS = logical

.DEFAULT_GOAL := help

install-dev-deps:
	uv sync --locked

install-deps:
	uv sync --locked --no-dev

fmt:
	uv run ruff check src --fix --unsafe-fixes
	uv run ruff format src
	uv run toml-sort pyproject.toml

LINT_TARGETS = \
	lint-django-checks \
	lint-django-migrations \
	lint-openapi-schema \
	lint-ruff-check \
	lint-ruff-format \
	lint-mypy \
	lint-dockerfile \
	lint-yaml \
	lint-toml \
	lint-markdown \
	lint-dotenv

lint:
	@$(MAKE) --no-print-directory -j $(LINT_TARGETS)

lint-django-checks:
	uv run python src/manage.py check

lint-django-migrations:
	uv run python src/manage.py makemigrations --check --dry-run --no-input

lint-openapi-schema:
	uv run python src/manage.py spectacular --api-version v1 --fail-on-warn > /dev/null

lint-ruff-check:
	uv run ruff check src

lint-ruff-format:
	uv run ruff format --check src

lint-mypy:
	uv run mypy -n 4 src

lint-toml:
	uv run toml-sort --check pyproject.toml

lint-markdown:
	uv run pymarkdown scan README.md

lint-dotenv:
	uv run dotenv-linter src/app/.env.ci

lint-dockerfile:
	@if command -v hadolint >/dev/null 2>&1; then \
		echo Running hadolint...; \
		hadolint Dockerfile; \
	else \
		echo "hadolint not found, skipping Dockerfile linting"; \
	fi

lint-yaml:
	@if command -v yamllint >/dev/null 2>&1; then \
		echo Running yamllint...; \
		yamllint .; \
	else \
		echo "yamllint not found, skipping YAML files linting"; \
	fi

test:
	@mkdir -p static  # be sure dir for static files exists
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
