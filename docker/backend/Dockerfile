FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TINI_VERSION=v0.19.0 \
    DOCKERIZE_VERSION=v0.6.1 \
    POETRY_HOME=/opt/poetry


ENV PATH="$POETRY_HOME/bin:$PATH"


RUN mkdir /code
WORKDIR /code
COPY poetry.lock pyproject.toml /code/
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y \
      curl \
      bash \
      build-essential \
      python3-pip \
      wget \
      gettext \
      libpq-dev \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi\
    # Installing `dockerize` utility: \
    # https://github.com/jwilder/dockerize
    && wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    # Cleaning cache:
    && apt-get remove -y python3-pip \
    && apt-get autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list
COPY ./src/backend /code/

COPY ./docker/backend/entrypoint.sh /docker-entrypoint.sh
RUN chmod +x '/docker-entrypoint.sh'

ENTRYPOINT ["/docker-entrypoint.sh"]

RUN python manage.py collectstatic --noinput
