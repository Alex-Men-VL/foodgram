FROM python:3.10-slim-buster AS development_build
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TINI_VERSION=v0.19.0 \
    DOCKERIZE_VERSION=v0.6.1 \
    POETRY_HOME=/opt/poetry

ENV PATH="$POETRY_HOME/bin:$PATH"

ARG DJANGO_ENV

RUN mkdir /code
RUN apt-get update \
    && apt-get install -y \
      curl \
      bash \
      wget \
    # Installing `poetry` package manager:
    # https://github.com/python-poetry/poetry
    && curl -sSL 'https://install.python-poetry.org' | python - \
    # Installing `dockerize` utility:
    # https://github.com/jwilder/dockerize
    && wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    # Cleaning cache:
    && apt-get autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list

WORKDIR /code

COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install \
        $(if [ "$DJANGO_ENV" = 'production' ]; then echo '--no-dev'; fi) \
        --no-interaction --no-ansi

COPY ./docker/backend/entrypoint.sh /docker-entrypoint.sh
RUN chmod +x '/docker-entrypoint.sh'

ENTRYPOINT ["/docker-entrypoint.sh"]


FROM development_build AS production_build
COPY ./src/backend /code
