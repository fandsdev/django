# My personal (very) opinionated django template

[![CircleCI](https://circleci.com/gh/f213/django.svg?style=svg&circle-token=8ce8cbe93d81d60af6b67c82a82563d93da0cb03)](https://circleci.com/gh/f213/django) ![Shields.io](https://img.shields.io/github/last-commit/f213/django?style=flat-square)

![Easy peasy](https://user-images.githubusercontent.com/1592663/79918184-93bca100-8434-11ea-9902-0ff726a864a3.gif)


## What is in the box

* API-only django (checkout [this post](https://t.me/pmdaily/257) in Russian) based on Django REST Framework
* Starter Circle CI configuration
* pytest with usefull stuff like freezegun, pytest-mock and super convinient [DRF test client](https://github.com/f213/django/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/src/app/tests/tests_health.py#L9)
* flake8 with ton of plugins (contact me if you know more)
* [pip-tools](https://github.com/jazzband/pip-tools) with separate development-time dependencies
* Custom [user model](https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#specifying-a-custom-user-model)
* [Whitenoise](http://whitenoise.evans.io) for effortless static files hosting
* Sentry. Set `SENTRY_DSN` env var if you need it.

## Installation

```
$ pip install cookiecutter
$ cookicutter gh:f213/django
```
