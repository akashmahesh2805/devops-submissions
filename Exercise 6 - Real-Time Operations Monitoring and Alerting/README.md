# Exercise 6 - Real-Time Operations Monitoring and Alerting

The Python exporter simulates delivery activity. Prometheus scrapes it, evaluates alert rules, and Grafana provisions a dashboard with total, pending, on-the-way, and average delivery-time panels.

## Run

```powershell
docker-compose -f docker-compose.yaml up -d --build
```

- Metrics: http://localhost:8000/metrics
- Prometheus targets and alerts: http://localhost:9090/targets and http://localhost:9090/alerts
- Grafana: http://localhost:3000 (complete the first-run sign-in prompt)

Prometheus uses the `delivery_service` target and evaluates `HighPendingDeliveries` and `HighAverageDeliveryTime`. The pending-delivery simulation intentionally varies around the alert threshold.

## Jenkins

Create a Pipeline job using this repository's `Jenkinsfile` at `Exercise 6 - Real-Time Operations Monitoring and Alerting/Jenkinsfile`. Its agent needs Docker CLI, Docker Compose, and access to the Docker daemon. The pipeline validates the Compose configuration, builds and starts the stack, and verifies the metrics endpoint.

Stop the stack with:

```powershell
docker-compose -f docker-compose.yaml down
```
