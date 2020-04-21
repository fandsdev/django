# My personal (very) opinionated django template

[![CircleCI](https://circleci.com/gh/f213/django.svg?style=svg&circle-token=8ce8cbe93d81d60af6b67c82a82563d93da0cb03)](https://circleci.com/gh/f213/django) ![Shields.io](https://img.shields.io/github/last-commit/f213/django?style=flat-square)

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
