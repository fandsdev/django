# My personal (very) opinionated django template

![Shields.io](https://img.shields.io/github/last-commit/fandsdev/django?style=flat-square) [![Maintainability](https://api.codeclimate.com/v1/badges/2b9800b10414a4ad2622/maintainability)](https://codeclimate.com/github/f213/django/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/2b9800b10414a4ad2622/test_coverage)](https://codeclimate.com/github/f213/django/test_coverage)

![Easy peasy](https://user-images.githubusercontent.com/1592663/79918184-93bca100-8434-11ea-9902-0ff726a864a3.gif)


## What is in the box

* API-only django (checkout [this post](https://t.me/pmdaily/257) in Russian) based on Django REST Framework with JWT support
* [pip-tools](https://github.com/jazzband/pip-tools) with separate development-time dependencies
* Strict type checking with mypy, [django-stubs](https://github.com/typeddjango/django-stubs) and [djangorestframework-stubs](https://github.com/typeddjango/djangorestframework-stubs)
* flake8 with ton of plugins (contact me if you know more)
* [black](https://github.com/psf/black) as uncompromising code formatter
* Starter CI configuration on GitHub Actions
* pytest with useful stuff like freezegun, pytest-mock and super convinient [DRF test client](https://github.com/f213/django/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/src/app/tests/tests_health.py#L9)
* Custom [user model](https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#specifying-a-custom-user-model)
* [drf-spectacular](https://github.com/tfranzel/drf-spectacular) for API Schema generation
* [django-axes](https://github.com/jazzband/django-axes) for additional security
* [Whitenoise](http://whitenoise.evans.io) for effortless static files hosting
* cloudflare-ready with [django-ipware](https://github.com/un33k/django-ipware)
* Sentry. Set `SENTRY_DSN` env var if you need it.
* Postgres ready. Set `DATABASE_URL` env var to something like `DATABASE_URL=postgres://postgres@localhost:5432/postgres`


## Optional next steps
You definetely should consider this steps after installation:
* Install [pytest-xdist](https://github.com/pytest-dev/pytest-xdist) if you plan to grow beyond 500 unittests
* If you are into docker, check out this [docker-compose.yml](https://github.com/f213/django/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/docker-compose.yml) to run on your machine


## Installation

```
$ pip install --upgrade cookiecutter
$ cookiecutter gh:fandsdev/django
```

## FAQ

### I have got an error «'random_ascii_string' is undefined»

You should upgrade cookiecutter to the latest version: `pip install --upgrade cookiecutter`

### I wanna hack this!

Thank you so much! Check out our [build pipeline](https://github.com/fandsdev/django/blob/master/Makefile) and pick any free [issue](https://github.com/fandsdev/django/issues).
