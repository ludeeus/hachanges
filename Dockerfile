FROM ludeeus/devcontainer:integration

WORKDIR /app
COPY . /app

RUN python3 -m pip install -r requirements.txt

CMD ["python3", "-u", "server.py"]
