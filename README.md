# fands.dev django template

![Shields.io](https://img.shields.io/github/last-commit/fandsdev/django?style=flat-square)

![Easy peasy](https://user-images.githubusercontent.com/1592663/79918184-93bca100-8434-11ea-9902-0ff726a864a3.gif)

## What is in the box

* API-only django (checkout [this post](https://t.me/pmdaily/257) in Russian) based on Django REST Framework with JWT support.
* [uv](https://docs.astral.sh/uv/) with separate development-time dependencies.
* Strict type checking with mypy, [django-stubs](https://github.com/typeddjango/django-stubs) and [djangorestframework-stubs](https://github.com/typeddjango/djangorestframework-stubs).
* tons of linters and formatters (contact us if any interesting linter is not included, see `Makefile` `fmt`, `lint` commands).
* Starter CI configuration on GitHub Actions.
* `pytest` with useful stuff like `freezegun`, `pytest-mock` and super convenient [DRF test client](https://github.com/fandsdev/django/blob/master/{{ cookiecutter.name }}/src/app/testing/api.py).
* Custom [user model](https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#specifying-a-custom-user-model).
* [drf-spectacular](https://github.com/tfranzel/drf-spectacular) for API Schema generation.
* [django-axes](https://github.com/jazzband/django-axes) for additional security.
* [Whitenoise](http://whitenoise.evans.io) for effortless static files hosting.
* Cloudflare ready with [django-ipware](https://github.com/un33k/django-ipware).
* Sentry. Set `SENTRY_DSN` env var if you need it.
* Postgres.

## Installation

You need [uv](https://docs.astral.sh/uv/), version >=0.6.0 (how to install [link](https://docs.astral.sh/uv/getting-started/installation/)).
It will install python 3.11 automatically if you don't have it yet.

We only support PostgreSQL as the database backend, so make sure it runs on `localhost:5432` before installing the project.

```bash
uvx cookiecutter gh:fandsdev/django
```

## FAQ

### I wanna hack this!

Thank you so much! Check out our [build pipeline](https://github.com/fandsdev/django/blob/master/Makefile) and pick any free [issue](https://github.com/fandsdev/django/issues).
