#
# Python version has to be set in the build command
#
ARG PYTHON_VERSION=python-version-not-set

#
# Compile custom uwsgi, cuz debian's one is weird
#
FROM python:${PYTHON_VERSION}-slim-bookworm AS uwsgi-compile
ENV _UWSGI_VERSION=2.0.31
RUN apt-get update && apt-get --no-install-recommends install -y build-essential wget && rm -rf /var/lib/apt/lists/*
RUN wget --progress=dot:giga -O uwsgi-${_UWSGI_VERSION}.tar.gz https://github.com/unbit/uwsgi/archive/${_UWSGI_VERSION}.tar.gz \
  && tar zxvf uwsgi-*.tar.gz \
  && UWSGI_BIN_NAME=/uwsgi make -C uwsgi-${_UWSGI_VERSION} \
  && rm -Rf uwsgi-*

#
# Build virtual environment with dependencies
# https://github.com/astral-sh/uv-docker-example/blob/main/multistage.Dockerfile
#
FROM python:${PYTHON_VERSION}-slim-bookworm AS deps-compile
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

WORKDIR /code

COPY pyproject.toml uv.lock /code/
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-dev

#
# Base image with django dependencies
# It is important to use the image that matches the deps-compile image
#
FROM python:${PYTHON_VERSION}-slim-bookworm AS base
LABEL maintainer="{{ cookiecutter.email }}"

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUTF8=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
    
ENV STATIC_ROOT=/code/static
# Define user ids to ensure consistent permissions, e.g., for mounted volumes
ENV UID=999 GID=999

RUN apt-get update \
  && apt-get --no-install-recommends install -y gettext locales-all tzdata git wait-for-it wget \
  && rm -rf /var/lib/apt/lists/*

RUN groupadd --system --gid=${GID} "web" \
  && useradd --system --uid=${UID} --gid=${GID} --create-home --home-dir "/code" "web"

COPY --from=uwsgi-compile /uwsgi /usr/local/bin/
COPY --from=deps-compile --chown=web:web /code/.venv /code/.venv
COPY --chown=web:web src /code/src
ENV PATH="/code/.venv/bin:$PATH"

WORKDIR /code/src

USER web
RUN python manage.py compilemessages \
  && python manage.py collectstatic --noinput


#
# web image
#
FROM base AS web
HEALTHCHECK --interval=15s --timeout=15s --start-period=15s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:8000/api/v1/healthchecks/

CMD ["sh", "-c", "python manage.py migrate && uwsgi --master --http=:8000 --venv=/code/.venv/ --wsgi=app.wsgi --workers=2 --threads=2 --harakiri=25 --max-requests=1000 --log-x-forwarded-for"]

#
# worker image
#
FROM base AS worker

ENV _CELERY_APP=app.celery
HEALTHCHECK --interval=15s --timeout=15s --start-period=5s --retries=3 \
  CMD celery --app=${_CELERY_APP} inspect ping --destination=celery@$HOSTNAME

CMD ["sh", "-c", "celery --app=${_CELERY_APP} worker --concurrency=${CONCURRENCY:-2} --hostname=celery@%h --max-tasks-per-child=${MAX_REQUESTS_PER_CHILD:-50} --time-limit=${TIME_LIMIT:-900} --soft-time-limit=${SOFT_TIME_LIMIT:-45}"]

#
# scheduler image
#
FROM base AS scheduler

ENV _SCHEDULER_DB_PATH=/var/db/scheduler
USER root
RUN mkdir --parent ${_SCHEDULER_DB_PATH} && chown web:web ${_SCHEDULER_DB_PATH}
USER web
VOLUME ${_SCHEDULER_DB_PATH}

ENV _CELERY_APP=app.celery
HEALTHCHECK NONE
CMD ["sh", "-c", "celery --app=${_CELERY_APP} beat --pidfile=/tmp/celerybeat.pid --schedule=${_SCHEDULER_DB_PATH}/celerybeat-schedule.db"]
