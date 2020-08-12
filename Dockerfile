FROM ludeeus/devcontainer:python

WORKDIR /app
COPY . /app

RUN python3 -m pip install -r requirements.txt

CMD ["python3", "-u", "server.py"]

HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost:9999/ || exit 1