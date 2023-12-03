ARG PYTHON_VERSION

FROM python:${PYTHON_VERSION}-slim-bookworm as uwsgi-compile

ENV _UWSGI_VERSION 2.0.22

RUN apt-get update && apt-get --no-install-recommends install -y build-essential wget && rm -rf /var/lib/apt/lists/*
RUN wget -O uwsgi-${_UWSGI_VERSION}.tar.gz https://github.com/unbit/uwsgi/archive/${_UWSGI_VERSION}.tar.gz \
  && tar zxvf uwsgi-*.tar.gz \
  && UWSGI_BIN_NAME=/uwsgi make -C uwsgi-${_UWSGI_VERSION} \
  && rm -Rf uwsgi-*

FROM python:${PYTHON_VERSION}-slim-bookworm as deps-compile

WORKDIR /
COPY poetry.lock pyproject.toml /

ARG POETRY_VERSION

RUN pip install --no-cache-dir poetry==${POETRY_VERSION}
RUN poetry export --format=requirements.txt > requirements.txt

FROM python:${PYTHON_VERSION}-slim-bookworm as base
LABEL maintainer="fedor@borshev.com"
LABEL com.datadoghq.ad.logs='[{"service": "django", "source": "uwsgi"}]'

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1
ENV STATIC_ROOT /var/lib/django-static
ENV _WAITFOR_VERSION 2.2.3

RUN apt-get update \
  && apt-get --no-install-recommends install -y gettext locales-all tzdata git wait-for-it wget \
  && rm -rf /var/lib/apt/lists/*

COPY --from=uwsgi-compile /uwsgi /usr/local/bin/
RUN pip install --no-cache-dir --upgrade pip

COPY --from=deps-compile /requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /src
COPY src /src

RUN ./manage.py makemessages --locale ru
RUN ./manage.py compilemessages
RUN ./manage.py collectstatic --noinput

FROM base as web
CMD ./manage.py migrate && uwsgi --master --http :8000 --module core.wsgi --workers 2 --threads 2 --harakiri 25 --max-requests 1000 --log-x-forwarded-for
