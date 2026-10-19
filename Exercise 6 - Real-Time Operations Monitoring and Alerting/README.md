# Exercise 6 - Real-Time Operations Monitoring and Alerting

The Python exporter simulates delivery activity. Prometheus scrapes it, evaluates alert rules, and Grafana provisions a dashboard with total, pending, on-the-way, and average delivery-time panels.

## Run

```powershell
docker compose -f docker-compose.yaml up -d --build
```

- Metrics: http://localhost:8000/metrics
- Prometheus targets and alerts: http://localhost:9090/targets and http://localhost:9090/alerts
- Grafana: http://localhost:3000 (complete the first-run sign-in prompt)

Prometheus uses the `delivery_service` target and evaluates `HighPendingDeliveries` and `HighAverageDeliveryTime`. Grafana provisions the Prometheus data source and the four-panel dashboard from the repository.

### Verify alert rules

Start the reproducible alert-test mode, which raises both pending counts and delivery times above the configured thresholds:

```powershell
docker compose -f docker-compose.yaml -f docker-compose.alert-test.yaml up -d --build
Start-Sleep -Seconds 30
Invoke-RestMethod http://localhost:9090/api/v1/alerts
```

Confirm `HighPendingDeliveries` and `HighAverageDeliveryTime` are both `firing`. In Prometheus, `http://localhost:9090/targets` should show `delivery_service` as **UP**; Grafana at `http://localhost:3000` should show the **Delivery Monitoring** dashboard with four panels. For normal randomized metrics instead, run the base Compose file alone.

## Jenkins

Create a Pipeline job using this repository's `Jenkinsfile` at `Exercise 6 - Real-Time Operations Monitoring and Alerting/Jenkinsfile`. Its agent needs Docker CLI with Compose v2 and access to the Docker daemon. The pipeline validates and builds the Compose stack, starts it in alert-test mode, then verifies the metrics endpoint and both firing alerts.

Stop the stack with:

```powershell
docker compose -f docker-compose.yaml -f docker-compose.alert-test.yaml down
```
