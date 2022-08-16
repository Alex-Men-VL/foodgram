#!/bin/sh

set -o errexit
set -o nounset
# shellcheck disable=SC2039
set -o pipefail

# Run python specific scripts:
# Running migrations in startup script might not be the best option, see:
# docs/pages/template/production-checklist.rst

# Start gunicorn:
# Docs: http://docs.gunicorn.org/en/stable/settings.html
gunicorn \
  --config python:docker.django.gunicorn_config \
  config.wsgi
