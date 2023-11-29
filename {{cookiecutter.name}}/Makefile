manage = poetry run src/manage.py

compilemessages: messages
	$(manage) compilemessages

fmt:
	poetry run autoflake --in-place --remove-all-unused-imports --recursive src tests
	poetry run isort src tests
	poetry run black src tests

lint:
	$(manage) check
	poetry run isort --check-only src tests
	poetry run black --check src tests
	poetry run flake8 src tests
	poetry run mypy src tests
	poetry run dotenv-linter src/core/.env.ci

messages:
	$(manage) makemessages --locale ru

test: compilemessages
	$(manage) makemigrations --dry-run --no-input --check
	poetry run pytest --dead-fixtures
	poetry run pytest -x

pr: fmt lint test
