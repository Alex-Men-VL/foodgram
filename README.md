# Foodgram website, "Food Assistant"

![Build status](https://github.com/Alex-Men-VL/foodgram/actions/workflows/main.yaml/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/Alex-Men-VL/foodgram/branch/main/graph/badge.svg?token=F22BFAXWLA)](https://codecov.io/gh/Alex-Men-VL/foodgram)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**Foodgram** is an online service where users can post recipes, subscribe to other users' publications,
add favorite recipes to their "Favorites" list, and download a summary list of products needed to prepare one or
more selected dishes before going to the store.


## Contents

- [Features](#features)
- [Development](#development)
  - [Prerequisites](#dev-prerequisites)
  - [Installation](#dev-installation)
  - [Testing](#dev-testing)
- [Production](#production)
  - [Deployment via docker compose](#prod-docker)
    - [Prerequisites](#prod-docker-prerequisites)
    - [Installation](#prod-docker-installation)
  - [Deployment via kubernetes](#prod-kuber)
- [Available environment variables](#envs)
- [Authors](#authors)
- [License](#license)
- [Thanks](#thanks)

<a name="features"></a>
## Features

- For `Django 3.2`
- Works with `Python 3.10`
- [12-Factor](http://12factor.net/) based settings via [django-environ](https://github.com/joke2k/django-environ)
- `Django REST framework 3.13`
- Supports `Postgres`
- Optimized development and production settings
- [Poetry](https://github.com/python-poetry/poetry) for managing dependencies
- Docker support using [docker-compose](https://github.com/docker/compose) for development and production
- Using [Nginx](https://nginx.org/ru/) on development and [Caddy](https://caddyserver.com/) on production
- `mypy` and `django-stubs` for static typing
- `flake8` for linting
- Tests
- [GitHub Actions](https://docs.github.com/en/actions) with full build, test, and deploy pipeline
- Serve static files on production from [Yandex Object Storage](https://cloud.yandex.ru/services/storage)

<a name="development"></a>
## Development

On development uses [Nginx](https://nginx.org/ru/) in conjunction with [Gunicorn](https://gunicorn.org/).

Static content is serving by nginx.

<a name="dev-prerequisites"></a>
### Prerequisites

The following tools should be installed:

- [Poetry](https://python-poetry.org/)
- [Docker-compose](https://docs.docker.com/compose/install/)

<a name="dev-installation"></a>
### Installation

Download the code and go into the repository:

```shell
$ git clone git@github.com:Alex-Men-VL/foodgram.git
$ cd foodgram
```

Create an .env file based on a template:

```shell
$ cp src/backend/.envs/.env.template src/backend/.envs/.env
```

[Change environment variables](#envs)

Start the project:

```shell
$ docker-compose up --build
```

Check container status:

```shell
$ docker ps -a
```

Expected result:

```shell
CONTAINER ID   IMAGE                   COMMAND                  CREATED              STATUS                          PORTS                    NAMES
222c66ea3eec   foodgram_nginx          "/docker-entrypoint.…"   About a minute ago   Up About a minute               0.0.0.0:80->80/tcp       foodgram-nginx-1
f5f7f90cc586   foodgram_backend:dev    "/docker-entrypoint.…"   About a minute ago   Up About a minute                                        foodgram-backend-1
c8ef80ae9232   postgres:12.0-alpine    "docker-entrypoint.s…"   About a minute ago   Up About a minute               0.0.0.0:5432->5432/tcp   foodgram-db-1
6152c7bf6fd1   foodgram_frontend:dev   "docker-entrypoint.s…"   About a minute ago   Exited (0) About a minute ago                            foodgram-frontend-1
```

In the new terminal, without shutting down the site, load test data into the database:

```shell
$ docker-compose exec db psql -U <db user name, default - foodgram_db_user> -f /backups/foodgram-test-data.sql
```

The site is available via links:

- [Main page](http://127.0.0.1/)
- [Admin panel](http://127.0.0.1/admin/)
- [API schema](http://127.0.0.1/api/docs/)

<a name="dev-testing"></a>
### Testing

#### Testing coding standards

Run `flake8` linter:

```shell
$ docker compose run --rm backend flake8
```

Run `mypy`:

```shell
$ docker compose run --rm backend mypy .
```

#### Django end to end testing

Tests cover API and models.

Run `Django tests`:

```shell
$ docker compose run --rm backend pytest
```

<a name="production"></a>
## Production

On development uses [Caddy](https://caddyserver.com/) in conjunction with [Gunicorn](https://gunicorn.org/).

Static content is serving by [Yandex Object Storage](https://cloud.yandex.ru/services/storage).

<a name="prod-docker"></a>
### Deployment via docker compose

<a name="prod-docker-prerequisites"></a>
#### Prerequisites

The following tools should be installed:

- [Docker-compose](https://docs.docker.com/compose/install/)

To use existing images:

```shell
$ export BACKEND_IMAGE=ghcr.io/alex-men-vl/foodgram/backend:latest
$ export FRONTEND_IMAGE=ghcr.io/alex-men-vl/foodgram/frontend:latest
```

<a name="prod-docker-installation"></a>
#### Installation

Download the code and go into the repository:

```shell
$ git clone git@github.com:Alex-Men-VL/foodgram.git
$ cd foodgram
```

Create an .env file based on a template:

```shell
$ cp src/backend/.envs/.env.template src/backend/.envs/.env
```

[Set environment variables](#envs)

Start the project:

```shell
$ docker-compose up
```

<a name="prod-kuber"></a>
### Deployment via kubernetes

TODO

<a name="envs"></a>
## Available environment variables

The list of used environment variables is specified in [.env.template](src/backend/.envs/.env.template).

<a name="authors"></a>
## Authors

- **Menshikov Aleksandr** — Site backend — [GitHub](https://github.com/Alex-Men-VL)

<a name="license"></a>
## License

MIT licensed. See the [LICENSE](LICENSE) file for more details.

<a name="thanks"></a>
## Thanks

[Yandex practicum](https://practicum.yandex.ru/profile/middle-python/) for the provided front for the site.
