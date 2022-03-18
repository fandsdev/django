FROM python:3.10.3-slim-bullseye
LABEL maintainer="fedor@borshev.com"

LABEL com.datadoghq.ad.logs='[{"source": "uwsgi", "service": "django"}]'

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

ENV STATIC_ROOT /static

ENV _UWSGI_VERSION 2.0.20

RUN echo deb http://deb.debian.org/debian bullseye contrib non-free > /etc/apt/sources.list.d/debian-contrib.list \
  && apt update \
  && apt --no-install-recommends install -y gettext locales-all wget \
  imagemagick tzdata wait-for-it build-essential \
  libxml2-dev libxslt1-dev libjpeg62-turbo-dev libjpeg-dev libfreetype6-dev \
  libtiff5-dev liblcms2-dev libwebp-dev tk8.6-dev \
  libffi-dev libcgraph6 libgraphviz-dev libmagic-dev libpq-dev \
  default-mysql-client default-libmysqlclient-dev \
  && rm -rf /var/lib/apt/lists/*

RUN wget -O uwsgi-${_UWSGI_VERSION}.tar.gz https://github.com/unbit/uwsgi/archive/${_UWSGI_VERSION}.tar.gz \
    && tar zxvf uwsgi-*.tar.gz \
    && UWSGI_BIN_NAME=/usr/local/bin/uwsgi make -C uwsgi-${_UWSGI_VERSION} \
    && rm -Rf uwsgi-*

RUN pip install --upgrade pip

ADD requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /src
ADD src /src

RUN ./manage.py compilemessages
RUN ./manage.py collectstatic --noinput

ARG RELEASE=dev-untagged
ENV SENTRY_RELEASE ${RELEASE}
ENV DD_VERSION ${RELEASE}

USER nobody

CMD uwsgi --master --http :8000 --module app.wsgi --workers 2 --threads 2 --harakiri 25 --max-requests 1000 --log-x-forwarded-for --buffer-size 32000
