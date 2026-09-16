# Flask Flash Sale — Kubernetes ReplicaSet

## Objective

This project demonstrates a simple Flask flash-sale application running inside a Kubernetes ReplicaSet on a single-node Minikube cluster. It highlights:

- Flask application behavior
- Docker containerization
- ReplicaSet creation
- Scaling from 3 replicas to 5
- Self-healing after a Pod is deleted
- Single-node pod placement

## Application Endpoints

- GET /  
  Returns a welcome message with the pod hostname and timestamp.

- GET /buy?user=123  
  Simulates a flash-sale purchase and returns the selected item, user, Pod hostname, and time.

- GET /health  
  Returns health status and the pod hostname for readiness/liveness checks.

## Architecture

Minikube
└── 1 Node
└── ReplicaSet
├── Pod 1
├── Pod 2
├── Pod 3
├── Pod 4
└── Pod 5

## Docker

The Flask app is packaged in a Docker image named `flashsale:1.0` and runs on port `5000` using Gunicorn.

## Kubernetes

The project uses a Kubernetes `ReplicaSet` with:

- initial replicas: 3
- labels: `app: flashsale`
- selector: `app: flashsale`
- service: `flashsale-svc`

## Scaling

The application starts with 3 replicas and can be scaled to 5 with:

```bash
kubectl scale rs flashsale-rs --replicas=5
```

## Self-Healing

If one pod is deleted, the ReplicaSet detects the mismatch and creates a replacement pod automatically.

## Verification Commands

```bash
kubectl apply -f flashsale-replicaset.yaml
kubectl get rs
kubectl get pods
kubectl get pods -o wide
kubectl logs <pod-name>
kubectl describe rs flashsale-rs
kubectl describe pod <pod-name>
```

## GitHub

This project is intended for a personal GitHub repository for assignment submission.
