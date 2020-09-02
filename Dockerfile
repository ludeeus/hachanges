FROM ludeeus/container:frontend

COPY . /app
WORKDIR /app

RUN \
  apk add curl \
  && cd /app/client \
  && yarn install \
  && yarn run build \
  && cd /app \
  && yarn install \
  && yarn run build

ENTRYPOINT ["yarn", "run", "start:prod"]

LABEL org.opencontainers.image.source = "https://github.com/ludeeus/hachanges"

HEALTHCHECK --interval=1m --timeout=10s \
  CMD curl --fail -sSL http://127.0.0.1:3000/110/json