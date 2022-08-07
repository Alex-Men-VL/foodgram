# Foodgram website, "Food Assistant"

---

**Foodgram** is an online service where users can post recipes, subscribe to other users' publications,
add favorite recipes to their "Favorites" list, and download a summary list of products needed to prepare one or
more selected dishes before going to the store.


## Contents

---

- [Features](#features)
- [Development](#development)
  - [Prerequisites](#dev-prerequisites)
  - [Installation](#dev-installation)
  - [Testing](#dev-testing)
  - [Available environment variables](#dev-envs)
- [Production](#production)
- [Authors](#authors)
- [License](#license)
- [Thanks](#thanks)

<a name="features"></a>
## Features

---

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

---

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

Start the project:

```shell
$ docker-compose up --build
```

Check container status:

```shell
$ docker ps
```

Expected result:

```shell
CONTAINER ID   IMAGE                  COMMAND                  CREATED             STATUS             PORTS                    NAMES
cd692f2bf19d   foodgram_nginx         "/docker-entrypoint.…"   About an hour ago   Up About an hour   0.0.0.0:80->80/tcp       foodgram-nginx-1
cfd0c78ccf21   foodgram_backend       "/docker-entrypoint.…"   About an hour ago   Up About an hour                            foodgram-backend-1
77ddcbe9d6e2   postgres:12.0-alpine   "docker-entrypoint.s…"   About an hour ago   Up About an hour   0.0.0.0:5432->5432/tcp   foodgram-db-1
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

<a name="dev-envs"></a>
### Available environment variables

TODO

<a name="production"></a>
## Production

---

TODO

<a name="authors"></a>
## Authors

---

- **Menshikov Aleksandr** — Site backend — [GitHub](https://github.com/Alex-Men-VL)

<a name="license"></a>
## License

---

MIT licensed. See the [LICENSE](LICENSE) file for more details.

<a name="thanks"></a>
## Thanks

---

[Yandex practicum](https://practicum.yandex.ru/profile/middle-python/) for the provided front for the site.
