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
    - [Prerequisites](#prod-kuber-prerequisites)
    - [Installation](#prod-kuber-installation)
    - [Deploy PostgreSQL in a cluster](#prod-kuber-db)
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
$ cp src/.envs/.env.template src/.envs/.env
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
CONTAINER ID   IMAGE                   COMMAND                  CREATED          STATUS                  PORTS                      NAMES
91bb9f1e2f4d   foodgram_nginx          "/docker-entrypoint.…"   8 seconds ago    Up Less than a second   0.0.0.0:80->80/tcp         foodgram-nginx-1
ab13c1bb8a07   foodgram_backend:dev    "/docker-entrypoint.…"   9 seconds ago    Up 2 seconds                                       foodgram-backend-1
90e56294f31e   postgres:12.0-alpine    "docker-entrypoint.s…"   9 seconds ago    Up 5 seconds            0.0.0.0:5432->5432/tcp     foodgram-db-1
8823462d857c   foodgram_frontend:dev   "docker-entrypoint.s…"   9 seconds ago    Up 5 seconds            127.0.0.1:3000->3000/tcp   foodgram-frontend-1
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

#### Django end-to-end testing

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
$ export BACKEND_IMAGE=ghcr.io/alex-men-vl/foodgram/backend:prod
$ export FRONTEND_IMAGE=ghcr.io/alex-men-vl/foodgram/frontend:prod
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
$ cp src/.envs/.env.template src/.envs/.env
```

[Set environment variables](#envs)

Start the project:

```shell
$ docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml up
```

Check container status:

```shell
$ docker ps -a
```

Expected result:

```shell
CONTAINER ID   IMAGE                    COMMAND                  CREATED              STATUS          PORTS                                                NAMES
227915090d1f   caddy:2.5.2              "caddy run --config …"   About a minute ago   Up 19 seconds   0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp, 2019/tcp   foodgram-caddy-1
c433ba699f05   foodgram_backend:prod    "/docker-entrypoint.…"   About a minute ago   Up 37 seconds                                                        foodgram-backend-1
c690c3735e12   postgres:12.0-alpine     "docker-entrypoint.s…"   About a minute ago   Up 48 seconds   5432/tcp                                             foodgram-db-1
4f61422d6ab6   foodgram_frontend:prod   "docker-entrypoint.s…"   About a minute ago   Up 48 seconds   127.0.0.1:3000->3000/tcp                             foodgram-frontend-1
```

The site is available via links:

- [Main page](http://127.0.0.1/)
- [Admin panel](http://127.0.0.1/admin/)
- [API schema](http://127.0.0.1/api/docs/)

<a name="prod-kuber"></a>
### Deployment via kubernetes

*Instructions written for deployment via Minikube.*

<a name="prod-kuber-prerequisites"></a>
#### Prerequisites

The following tools should be installed:

- [kubectl](https://kubernetes.io/ru/docs/tasks/tools/install-kubectl/);
- [Minikube](https://minikube.sigs.k8s.io/docs/start/);
- [VirtualBox](https://www.virtualbox.org/);
- Database deployed separately from the Kubernetes cluster or [via helm](#prod-kuber-db).

<a name="prod-kuber-installation"></a>
#### Installation

Download the code and go into the repository:

```shell
$ git clone git@github.com:Alex-Men-VL/foodgram.git
$ cd foodgram/kubernetes/prod
```

Start minikube cluster with [VirtualBox driver](https://minikube.sigs.k8s.io/docs/drivers/virtualbox/):

```shell
$ minikube start --driver=virtualbox
```

Get all worker nodes:

```shell
$ kubectl get nodes
```

Expected result:

```shell
NAME       STATUS   ROLES                  AGE    VERSION
minikube   Ready    control-plane,master   2h     v1.23.3
```

Create namespace:

```shell
$ kubectl create namespace foodgram-prod
```

Create Secrets:

Set **encoded** environment variables from [.env.template](src/.envs/.env.template)
in [secrets.yaml](kubernetes/prod/secrets.yaml).

Variables must be encoded as shown below.

```shell
$ echo -n 'variable_value' | base64
```

You would see the encoded value as outputs as shown below.

```shell
YWRtaW5fcGFzc3dvcmQ=
```

Enter these values in yaml file.

```yaml
...
secret_key: YWRtaW5fcGFzc3dvcmQ=
...
```

Execute the below command so that the secrets are available within the Kubernetes cluster during run time.

```shell
kubectl apply -f secrets.yaml
```

You would see the below message.

```shell
secret/django created
secret/aws created
```

Enable the minikube ingress addon:

```shell
$ minikube addons enable ingress
```

Start the project:

```shell
$ ./deploy.sh
```

You would see the below message.

```shell
Run deploy

configmap/web-configmap created
job.batch/django-job created
cronjob.batch/django-clearsessions created
deployment.apps/django-deployment created
service/django-service created
deployment.apps/react-deployment created
service/react-service created
ingress.networking.k8s.io/ingress-service created

Project deployed successfully
```

List all pods in the namespace:

```shell
$ kubectl get pods
```

Expected result:

```shell
NAME                                READY   STATUS      RESTARTS   AGE
django-deployment-cf468dbc5-hcwmg   1/1     Running     0          48s
django-job-b2p58                    0/1     Completed   0          49s
react-deployment-654f4749b-vwxx5    1/1     Running     0          47s
```

Add the following line to the end of the `hosts` file on your computer (requires admin rights):

```shell
<minikube ip> star-burger.test
```

Path to the `hosts` file:

- `Windows10` - C:\Windows\System32\drivers\etc\hosts
- `Linux` - /etc/hosts
- `Mac OS X` - /private/etc/hosts

To get `minikube ip` use the following command:

```shell
minikube ip
```

The site is available via links:

- [Main page](http://foodgram.test/)
- [Admin panel](http://foodgram.test/admin/)

To get pod logs use the following command:

```shell
$ kubectl logs <POD name>
```

<a name="prod-kuber-db"></a>
#### Deploy PostgreSQL in a cluster

> If possible, it is better to use external databases, put them on a separate VPS, or order a separate
Managed Database service from the host.

Install [helm](https://helm.sh/docs/intro/install/).

Add the necessary chart and install it with the following commands.

```shell
$ helm repo add bitnami https://charts.bitnami.com/bitnami
$ helm install <host name> bitnami/postgresql
```

The terminal will display an instruction to get the password from the database and a command to connect to it.
Connect to the database following the instructions.

Create a new database and user:

```shell
CREATE DATABASE <db_name>;
CREATE USER <db_user> WITH ENCRYPTED PASSWORD <'db_password'>;
GRANT ALL PRIVILEGES ON DATABASE <db_name> TO <db_user>;
```

Specify this values in the file with secrets.

<a name="envs"></a>
## Available environment variables

The list of used environment variables is specified in [.env.template](src/.envs/.env.template).

<a name="authors"></a>
## Authors

- **Menshikov Aleksandr** — Site backend — [GitHub](https://github.com/Alex-Men-VL)

<a name="license"></a>
## License

MIT licensed. See the [LICENSE](LICENSE) file for more details.

<a name="thanks"></a>
## Thanks

[Yandex practicum](https://practicum.yandex.ru/profile/middle-python/) for the provided front for the site.
