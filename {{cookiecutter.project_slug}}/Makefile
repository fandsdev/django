manage = poetry run src/manage.py

fmt:
	poetry run autoflake --in-place --remove-all-unused-imports --recursive src tests
	poetry run black src tests

lint:
	$(manage) check
	poetry run flake8 src tests
	poetry run mypy src tests
	poetry run dotenv-linter src/core/.env.ci

test:
	mkdir -p src/static

	$(manage) makemigrations --dry-run --no-input --check
	$(manage) compilemessages
	poetry run pytest --dead-fixtures
	poetry run pytest -x

pr: fmt lint test
