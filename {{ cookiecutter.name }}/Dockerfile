#
# Python version has to be set in the build command
#
ARG PYTHON_VERSION=python-version-not-set

#
# Compile custom uwsgi, cuz debian's one is weird
#
FROM python:${PYTHON_VERSION}-slim-bookworm AS uwsgi-compile
ENV _UWSGI_VERSION=2.0.24
RUN apt-get update && apt-get --no-install-recommends install -y build-essential wget && rm -rf /var/lib/apt/lists/*
RUN wget -O uwsgi-${_UWSGI_VERSION}.tar.gz https://github.com/unbit/uwsgi/archive/${_UWSGI_VERSION}.tar.gz \
  && tar zxvf uwsgi-*.tar.gz \
  && UWSGI_BIN_NAME=/uwsgi make -C uwsgi-${_UWSGI_VERSION} \
  && rm -Rf uwsgi-*

#
# Build dependencies with uv
# https://github.com/astral-sh/uv-docker-example/blob/main/multistage.Dockerfile
#
FROM python:${PYTHON_VERSION}-slim-bookworm AS deps-compile
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

#
# Base image with django dependencies
# It is important to use the image that matches the deps-compile image
#
FROM python:${PYTHON_VERSION}-slim-bookworm AS base
LABEL maintainer="{{ cookiecutter.email }}"

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV STATIC_ROOT=/var/lib/django-static

RUN apt-get update \
  && apt-get --no-install-recommends install -y gettext locales-all tzdata git wait-for-it wget \
  && rm -rf /var/lib/apt/lists/*

COPY --from=uwsgi-compile /uwsgi /usr/local/bin/
COPY --from=deps-compile /app/src /app/src
COPY --from=deps-compile /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app/src

RUN chmod +x ./manage.py
RUN ./manage.py compilemessages
RUN ./manage.py collectstatic --noinput

# Also to mark that when CMD is used in shell form, it is a conscious decision
SHELL ["/bin/bash", "-c"]


FROM base AS web
HEALTHCHECK --interval=15s --timeout=15s --start-period=15s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:8000/api/v1/healthchecks/

CMD ./manage.py migrate && uwsgi --master --http :8000 --venv /app/.venv/ --module app.wsgi --workers 2 --threads 2 --harakiri 25 --max-requests 1000 --log-x-forwarded-for


FROM base AS worker

ENV _CELERY_APP=app.celery
HEALTHCHECK --interval=15s --timeout=15s --start-period=5s --retries=3 \
  CMD celery --app=${_CELERY_APP} inspect ping --destination=celery@$HOSTNAME

CMD celery --app=${_CELERY_APP} worker --concurrency=${CONCURENCY:-2} --hostname="celery@%h" --max-tasks-per-child=${MAX_REQUESTS_PER_CHILD:-50} --time-limit=${TIME_LIMIT:-900} --soft-time-limit=${SOFT_TIME_LIMIT:-45}


FROM base AS scheduler

ENV _SCHEDULER_DB_PATH=/var/db/scheduler
USER root
RUN mkdir -p ${_SCHEDULER_DB_PATH} && chown nobody ${_SCHEDULER_DB_PATH}
VOLUME ${_SCHEDULER_DB_PATH}
USER nobody

ENV _CELERY_APP=app.celery
HEALTHCHECK NONE
CMD celery --app=${_CELERY_APP} beat --pidfile=/tmp/celerybeat.pid --schedule=${_SCHEDULER_DB_PATH}/celerybeat-schedule.db
