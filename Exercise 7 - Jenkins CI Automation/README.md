# Exercise 7 - Jenkins CI Automation

Run Jenkins in Docker with persistent home data.

## Run

```powershell
docker compose up -d
docker compose ps
```

Open http://localhost:8080 and follow the setup wizard. Retrieve the initial unlock password without saving it in the repository:

```powershell
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Install the suggested plugins to create the Freestyle and Pipeline jobs used by the following exercises. Jenkins data persists in the `jenkins_home` volume.
