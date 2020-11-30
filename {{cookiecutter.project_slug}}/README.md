# Django project

This project is bootstrapped using [f213/django](http://github.com/f213/django) template. [Drop a line](https://github.com/f213/django/issues) if you have some issues.

## Project structure

The main django app is called `app`. It contains `.env` file for django-environ. For examples see `src/app/.env.ci`. Here are some usefull app-wide tools:
* `app.admin` — app-wide django-admin customizations (empty yet), check out usage [examples](https://github.com/f213/django/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/src/app/admin)
* `app.viewset` — default viewset with [per-action serializers](https://github.com/f213/django/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/src/app/viewsets.py#L13-L28)
* `app.test.api_client` (available as `api` and `anon` fixtures within pytest) — a [convinient DRF test client](https://github.com/f213/django/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/src/users/tests/tests_whoami.py#L6-L16).

Django user model is located in the separate `users` app.

Also, feel free to add as much django apps as you want.

## Installing on a local machine
This project requires python 3.8. Deps are managed by [pip-tools](https://github.com/jazzband/pip-tools)

Install requirements:

```bash
$ pip install --upgrade pip pip-tools
$ make
$ cd src && cp app/.env.ci app/.env  # default environment variables
```

```bash
$ ./manage.py migrate
$ ./manage.py createsuperuser
```

Testing:
```bash
# run unit tests
$ pytest
```

Development servers:

```bash
# run django dev server
$ ./manage.py runserver

```

## Backend Code requirements

### Style

* Obey [django's style guide](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/#model-style).
* Configure your IDE to use [flake8](https://pypi.python.org/pypi/flake8) for checking your python code. For running flake8 manualy, do `cd src && flake8`
* Prefer English over your native language in comments and commit messages.
* Commit messages should contain the unique id of issue they are linked to (refs #100500)
* Every model and a model method should have a docstring.

### Code organisation

* KISS and DRY.
* Obey [django best practices](http://django-best-practices.readthedocs.io/en/latest/index.html).
* **No logic is allowed within the views or serializers**. Only models and services. When a model grows beyond 500 lines of code — create a service for that.
* Use PEP-484 [type hints](https://www.python.org/dev/peps/pep-0484/) when possible.
* Prefer composition over inheritance.
* Prefer [Manager](https://docs.djangoproject.com/en/3.0/topics/db/managers/) methods over static models methods.
* Do not use [signals](https://docs.djangoproject.com/en/3.0/topics/signals/) or [GenericRelations](https://docs.djangoproject.com/en/3.0/ref/contrib/contenttypes/) in your own code.
* No l10n is allowed in python code, use [django translation](https://docs.djangoproject.com/en/3.0/topics/i18n/translation/).
