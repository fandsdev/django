# My personal (very) opinionated django template

[![CircleCI](https://circleci.com/gh/f213/django.svg?style=svg&circle-token=8ce8cbe93d81d60af6b67c82a82563d93da0cb03)](https://circleci.com/gh/f213/django) ![Shields.io](https://img.shields.io/github/last-commit/f213/django?style=flat-square) [![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=f213/django)](https://dependabot.com) [![Maintainability](https://api.codeclimate.com/v1/badges/2b9800b10414a4ad2622/maintainability)](https://codeclimate.com/github/f213/django/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/2b9800b10414a4ad2622/test_coverage)](https://codeclimate.com/github/f213/django/test_coverage)

![Easy peasy](https://user-images.githubusercontent.com/1592663/79918184-93bca100-8434-11ea-9902-0ff726a864a3.gif)


## What is in the box

* API-only django (checkout [this post](https://t.me/pmdaily/257) in Russian) based on Django REST Framework with JWT support
* [drf-yasg](https://github.com/axnsan12/drf-yasg#drf-yasg---yet-another-swagger-generator) for API Schema generation
* [pip-tools](https://github.com/jazzband/pip-tools) with separate development-time dependencies
* Starter Circle CI configuration
* pytest with usefull stuff like freezegun, pytest-mock and super convinient [DRF test client](https://github.com/f213/django/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/src/app/tests/tests_health.py#L9)
* flake8 with ton of plugins (contact me if you know more)
* Custom [user model](https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#specifying-a-custom-user-model)
* [Whitenoise](http://whitenoise.evans.io) for effortless static files hosting
* Sentry. Set `SENTRY_DSN` env var if you need it.
* cloudflare-ready with [django-ipware](https://github.com/un33k/django-ipware)

## Optional next steps
You definetely should consider this steps after installation:
* Install [pytest-xdist](https://github.com/pytest-dev/pytest-xdist) if you plan to grow beyond 500 unittests
* If you are into docker, check out [bundled docker-compose.yml](https://github.com/f213/django/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/docker-compose.yml) to run on your machine


## Installation

```
$ pip install --upgrade cookiecutter
$ cookiecutter gh:f213/django
```

## FAQ

### I have got an error «'random_ascii_string' is undefined»

You should upgrade cookiecutter to the latest version: `pip install --upgrade cookiecutter`
