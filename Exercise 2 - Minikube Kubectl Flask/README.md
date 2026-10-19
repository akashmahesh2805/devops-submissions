# Exercise 2 - Minikube Kubectl Flask

Build and deploy a Flask application to Minikube with a single-replica Deployment and a Service on port `15000`.

## Run

From this directory in PowerShell:

```powershell
minikube start
minikube image build -t flask-app:latest .
kubectl apply -f flask-deployment.yaml
kubectl get deployments,pods,services
minikube service flask-app-service --url
```

Open the printed URL; the response should be `Hello from Flask on Kubernetes!`. The Service's port and target port are both `15000`.
