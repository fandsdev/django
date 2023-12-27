# fands.dev django template

![Shields.io](https://img.shields.io/github/last-commit/fandsdev/django?style=flat-square)

![Easy peasy](https://user-images.githubusercontent.com/1592663/79918184-93bca100-8434-11ea-9902-0ff726a864a3.gif)

## What is in the box

* API-only django (checkout [this post](https://t.me/pmdaily/257) in Russian) based on Django REST Framework with JWT support.
* [poetry](https://python-poetry.org) with separate development-time dependencies.
* Strict type checking with mypy, [django-stubs](https://github.com/typeddjango/django-stubs) and [djangorestframework-stubs](https://github.com/typeddjango/djangorestframework-stubs).
* tons of linters and formatters (contact me if something interesting not included, see `Makefile` `fmt`, `lint` commands).
* Starter CI configuration on GitHub Actions.
* `pytest` with useful stuff like `freezegun`, `pytest-mock` and super convinient [DRF test client](https://github.com/fandsdev/django/blob/master/%7B%7Bcookiecutter.name%7D%7D/src/tests/core/tests_health.py#L9)
* Custom [user model](https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#specifying-a-custom-user-model).
* [drf-spectacular](https://github.com/tfranzel/drf-spectacular) for API Schema generation.
* [django-axes](https://github.com/jazzband/django-axes) for additional security.
* [Whitenoise](http://whitenoise.evans.io) for effortless static files hosting.
* cloudflare-ready with [django-ipware](https://github.com/un33k/django-ipware).
* Sentry. Set `SENTRY_DSN` env var if you need it.
* Postgres ready. Set `DATABASE_URL` env var to something like `DATABASE_URL=postgres://postgres@localhost:5432/postgres`.

## Optional next steps

You definetely should consider this steps after installation:

* If you are into docker, check out this [docker-compose.yml](https://github.com/fandsdev/django/blob/master/%7B%7Bcookiecutter.name%7D%7D/docker-compose.yml) to run on your machine.

## Installation

```bash
poetry install

poetry run cookiecutter gh:fandsdev/django
```

## FAQ

### I have got an error «'random_ascii_string' is undefined»

You should upgrade cookiecutter to the latest version: `pip install --upgrade cookiecutter`.

### I wanna hack this!

Thank you so much! Check out our [build pipeline](https://github.com/fandsdev/django/blob/master/Makefile) and pick any free [issue](https://github.com/fandsdev/django/issues).
