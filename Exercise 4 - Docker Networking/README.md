# Exercise 4 - Docker Networking

Run a Flask API, MySQL, and Redis on one Docker bridge network. Compose creates the `my-bridge-net` bridge and makes the database containers discoverable by the names `mysql` and `redis`. MySQL requires a non-empty local root password; no password is stored in Git.

## Run and verify

```powershell
Copy-Item .env.example .env
# Replace the example value in .env with a unique local password.
docker compose up -d --build
docker compose ps
docker network inspect my-bridge-net
Invoke-RestMethod http://localhost:5001/about
docker compose exec flask python -c "import socket; [socket.create_connection((host, port), timeout=5).close() for host, port in [('mysql', 3306), ('redis', 6379)]]; print('Connected to mysql and redis')"
```

Verify that all three services are running/healthy, `/about` returns the API name, version, and description, and the Flask container prints `Connected to mysql and redis`. Containers use the isolated lab bridge; MySQL and Redis ports are not published to the host. `.env` is git-ignored; do not force-add it.

Stop the containers and remove the network with:

```powershell
docker compose down
```

Remove the local password file when no longer needed:

```powershell
Remove-Item .env
```
