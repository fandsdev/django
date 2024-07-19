ARG PYTHON_VERSION

#
# Compile custom uwsgi, cuz debian's one is weird
#
FROM python:${PYTHON_VERSION}-slim-bookworm as uwsgi-compile
ENV _UWSGI_VERSION 2.0.24
RUN apt-get update && apt-get --no-install-recommends install -y build-essential wget && rm -rf /var/lib/apt/lists/*
RUN wget -O uwsgi-${_UWSGI_VERSION}.tar.gz https://github.com/unbit/uwsgi/archive/${_UWSGI_VERSION}.tar.gz \
  && tar zxvf uwsgi-*.tar.gz \
  && UWSGI_BIN_NAME=/uwsgi make -C uwsgi-${_UWSGI_VERSION} \
  && rm -Rf uwsgi-*

#
# Build poetry and export compiled dependecines as plain requirements.txt
#
FROM python:${PYTHON_VERSION}-slim-bookworm as deps-compile

WORKDIR /
COPY poetry.lock pyproject.toml /

# Version is taken from poetry.lock, assuming it is generated with up-to-date version of poetry
RUN pip install --no-cache-dir poetry==$(cat poetry.lock |head -n1|awk -v FS='(Poetry |and)' '{print $2}')
RUN poetry export --format=requirements.txt > requirements.txt

#
# Base image with django dependecines
#
FROM python:${PYTHON_VERSION}-slim-bookworm as base
LABEL maintainer="fedor@borshev.com"

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1
ENV STATIC_ROOT /var/lib/django-static

RUN apt-get update \
  && apt-get --no-install-recommends install -y gettext locales-all tzdata git wait-for-it wget \
  && rm -rf /var/lib/apt/lists/*

COPY --from=uwsgi-compile /uwsgi /usr/local/bin/
COPY --from=deps-compile /requirements.txt /

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /src
COPY src /src

RUN chmod +x ./manage.py
RUN ./manage.py compilemessages
RUN ./manage.py collectstatic --noinput

FROM base as web
CMD ./manage.py migrate && uwsgi --master --http :8000 --module app.wsgi --workers 2 --threads 2 --harakiri 25 --max-requests 1000 --log-x-forwarded-for


FROM base as worker

ENV _CELERY_APP=app.celery
HEALTHCHECK --interval=15s --timeout=15s --start-period=5s --retries=3 \
  CMD celery -A ${_CELERY_APP} inspect ping -d celery@$HOSTNAME

CMD celery -A ${_CELERY_APP} worker -c ${CONCURENCY:-2} -n "celery@%h" --max-tasks-per-child ${MAX_REQUESTS_PER_CHILD:-50} --time-limit ${TIME_LIMIT:-900} --soft-time-limit ${SOFT_TIME_LIMIT:-45}


FROM base as scheduler

ENV _SCHEDULER_DB_PATH=/var/db/scheduler
USER root
RUN mkdir -p ${_SCHEDULER_DB_PATH} && chown nobody ${_SCHEDULER_DB_PATH}
VOLUME ${_SCHEDULER_DB_PATH}
USER nobody

ENV _CELERY_APP=app.celery
HEALTHCHECK NONE
CMD celery -A ${_CELERY_APP} beat --pidfile=/tmp/celerybeat.pid --schedule=${_SCHEDULER_DB_PATH}/celerybeat-schedule.db
