# hachanges

1. Clone 
2. Build

```bash
sudo docker build --tag=hachanges .
```

3. Run

```bash
sudo docker run -d --name hachanges -p 9999:9999 -e GHTOKEN=dfkjhs783huf hachanges
```