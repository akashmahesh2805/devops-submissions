# Exercise 3 - Minikube Scaling Flask App with Replicasets

Build the Flask flash-sale app as a local Minikube image and deploy it as a three-replica ReplicaSet. The Service exposes `/`, `/buy`, and `/health`.

## Run

From this directory in PowerShell:

```powershell
minikube start
minikube image build -t flashsale:1.0 .
kubectl apply -f flashsale-replicaset.yaml
kubectl get rs,pods
kubectl scale rs flashsale-rs --replicas=5
kubectl get rs,pods -o wide
```

Delete one Pod to verify self-healing; the ReplicaSet should replace it and maintain five replicas:

```powershell
kubectl delete pod <pod-name>
kubectl get pods
```

To test the Service, run `kubectl port-forward service/flashsale-svc 8080:80` and open `http://localhost:8080/` or `http://localhost:8080/buy?user=123`.
