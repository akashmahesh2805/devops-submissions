# Exercise 1 - Kubernetes Getting Started

Deploy an Nginx Pod and expose it with a NodePort Service on Minikube.

## Run

```powershell
minikube start
kubectl apply -f hello-k8s.yaml
kubectl get pods,services
minikube service hello-k8s
```

The service opens the Nginx welcome page. The Pod and Service are both defined in `hello-k8s.yaml`.
