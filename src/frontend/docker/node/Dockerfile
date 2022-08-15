ARG NODE_VERSION=14.17.3

FROM node:${NODE_VERSION}-alpine as builder

WORKDIR /app

COPY /src/frontend/package*.json /app/

RUN npm install

COPY /src/frontend /app

RUN npm run build

# ---------------------------------------------------------------

FROM node:${NODE_VERSION}-alpine

WORKDIR /app

RUN npm install -g serve

COPY --from=builder /app/build ./build
