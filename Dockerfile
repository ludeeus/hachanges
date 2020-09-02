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

HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost:3000/ || exit 1