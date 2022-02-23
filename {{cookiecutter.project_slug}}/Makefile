install-dev-deps: dev-deps
	pip-sync requirements.txt dev-requirements.txt

install-deps: deps
	pip-sync requirements.txt

deps:
	pip-compile requirements.in

dev-deps: deps
	pip-compile dev-requirements.in

lint:
	flake8 src
	cd src && mypy

test:
	cd src && pytest --dead-fixtures
	cd src && pytest -x
