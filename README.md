# My personal (very) opinionated django template

## What is in the box

* API-only django (checkout [this post](https://t.me/pmdaily/257) in Russian) based on Django REST Framework
* [pip-tools](https://github.com/jazzband/pip-tools) with separate dev-dependencies
* pytest
* Pre-installed Circle CI configuration
* Custom [user model](https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#specifying-a-custom-user-model)
* [Whitenoise](http://whitenoise.evans.io) for effortless staticfiles hosting
* Sentry (set `SENTRY_DSN` environment variable)

## Installation

```
$ pip install cookiecutter
$ cookicutter gh:f213/django
```
