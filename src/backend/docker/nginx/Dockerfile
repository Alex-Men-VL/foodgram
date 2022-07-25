FROM nginx:1.19.3

ARG DJANGO_ENV

COPY ./src/backend/docker/nginx/$DJANGO_ENV/default.conf /etc/nginx/conf.d/default.conf
