# Exercise 4 - Docker Networking

Run a Flask API, MySQL, and Redis on one Docker bridge network. Compose creates the `my-bridge-net` bridge and makes the database containers discoverable by the names `mysql` and `redis`.

## Run and verify

```powershell
docker compose up -d --build
docker network inspect my-bridge-net
Invoke-RestMethod http://localhost:5001/about
docker compose exec flask python -c "import socket; [socket.create_connection((host, port), timeout=5).close() for host, port in [('mysql', 3306), ('redis', 6379)]]; print('Connected to mysql and redis')"
```

The API returns its name, version, and description at `/about`. Containers use the isolated lab bridge; MySQL and Redis ports are not published to the host.

Stop the containers and remove the network with:

```powershell
docker compose down
```
