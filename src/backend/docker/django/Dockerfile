ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}-slim-buster AS base
ENV TINI_VERSION=v0.19.0 \
    DOCKERIZE_VERSION=v0.6.1 \
    VIRTUAL_ENV=/opt/venv \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.14 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/var/cache/pypoetry \
    POETRY_HOME=/usr/local

ARG DJANGO_ENV

SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
      bash \
      curl \
      wget \
    # Installing `poetry` package manager:
    # https://github.com/python-poetry/poetry
    && curl -sSL 'https://install.python-poetry.org' | python - \
    && poetry --version \
    # Installing `dockerize` utility:
    # https://github.com/jwilder/dockerize
    && wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && dockerize --version\
    # Activate environment
    && python -m venv ${VIRTUAL_ENV}

WORKDIR /

# Install requirements
COPY poetry.lock pyproject.toml ./
RUN poetry export \
      $(if [ "$DJANGO_ENV" = 'development' ]; then echo '--dev'; fi) \
      --without-hashes -o requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip ${VIRTUAL_ENV}/bin/pip install -r requirements.txt

# ---------------------------------------------------------------

FROM python:${PYTHON_VERSION}-slim-bullseye AS development_build

ARG APP_ROOT=/code
ARG APP_USER=web
ARG UID=1000
ARG GID=1000
ARG COVERAGE_DIR=/code/coverage

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    VIRTUAL_ENV=/opt/venv

ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}

RUN groupadd -g "${GID}" -r ${APP_USER} \
    # Root directory
    && useradd -d ${APP_ROOT} -g ${APP_USER} -l -r -u "${UID}" ${APP_USER} \
    && chown ${APP_USER}:${APP_USER} -R ${APP_ROOT} \
    # Static and media files:
    && mkdir -p '/var/www/django/static' '/var/www/django/media' \
    && chown ${APP_USER}:${APP_USER} '/var/www/django/static' '/var/www/django/media' \
    # Directory with reqs
    && mkdir -p ${VIRTUAL_ENV} \
    && chown ${APP_USER}:${APP_USER} ${VIRTUAL_ENV} \
    # Directory for coverage report
    && mkdir -p ${COVERAGE_DIR} \
    && chown ${APP_USER}:${APP_USER} -R ${COVERAGE_DIR}

COPY ./src/backend/docker/django/entrypoint.sh /docker-entrypoint.sh
RUN chmod +x '/docker-entrypoint.sh'

COPY --from=base --chown=${APP_USER}:${APP_USER} ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --from=base --chown=${APP_USER}:${APP_USER} /usr/local/bin/dockerize /usr/local/bin/dockerize

USER ${APP_USER}

ENTRYPOINT ["/docker-entrypoint.sh"]

# ---------------------------------------------------------------

FROM development_build AS production_build

ARG APP_ROOT=/code
ARG APP_USER=web

COPY --chown=${APP_USER}:${APP_USER} ./src/backend ${APP_ROOT}
