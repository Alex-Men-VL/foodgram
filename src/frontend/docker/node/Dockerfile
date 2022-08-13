FROM node:14.17.3-alpine as builder

WORKDIR /app

COPY /src/frontend/package*.json /app/

RUN npm install

COPY /src/frontend /app

RUN npm run build

# ---------------------------------------------------------------

FROM node:14.17.3-alpine

WORKDIR /app

RUN npm install -g serve

COPY --from=builder /app/build ./build
