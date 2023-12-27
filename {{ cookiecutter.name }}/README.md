# Django project

This project is bootstrapped using [fandsdev/django](http://github.com/fandsdev/django) template. [Drop a line](https://github.com/fandsdev/django/issues) if you have some issues.

## Project structure

The main django app is called `core`. It contains `.env` file for django-environ. For examples see `src/core/.env.ci`. Here are some usefull app-wide tools:

* `core.admin` — app-wide django-admin customizations (empty yet), check out usage [examples](https://github.com/fandsdev/django/tree/master/%7B%7Bcookiecutter.name%7D%7D/src/core/admin)
* `core.test.api_client` (available as `api` and `anon` fixtures within pytest) — a [convinient DRF test client](https://github.com/fandsdev/django/blob/master/%7B%7Bcookiecutter.name%7D%7D/src/tests/apps/users/tests_whoami.py#L6-L16).

Django user model is located in the separate `users` app.

Also, feel free to add as much django apps as you want.

## Installing on a local machine

This project requires python 3.11. Deps are managed by [poetry](https://python-poetry.org).

Install requirements:

```bash
poetry install
```

Run the server:

```bash
cp src/core/.env.ci src/core/.env

poetry run python src/manage.py migrate
poetry run python src/manage.py createsuperuser
poetry run python src/manage.py runserver
```

Useful commands

```bash
make fmt  # run code formatters

make lint  # run code quality checks

make test  # run tests
```

## Backend code requirements

### Style

* Obey [django's style guide](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/#model-style).
* Configure your IDE to use [flake8](https://pypi.python.org/pypi/flake8) for checking your python code. To run our linters manualy, do `make lint`.
* Prefer English over your native language in comments and commit messages.
* Commit messages should contain the unique id of issue they are linked to (refs #100500).
* Every model, service and model method should have a docstring.

### Code organisation

* KISS and DRY.
* Obey [django best practices](http://django-best-practices.readthedocs.io/en/latest/index.html).
* **No logic is allowed within the views or serializers**. Only services and models. When a model grows beyond 500 lines of code — go create some services.
* Use PEP-484 [type hints](https://www.python.org/dev/peps/pep-0484/) when possible.
* Prefer composition over inheritance.
* Never use [signals](https://docs.djangoproject.com/en/dev/topics/signals/) or [GenericRelations](https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/) in your own code.
* No l10n is allowed in python code, use [django translation](https://docs.djangoproject.com/en/dev/topics/i18n/translation/).
