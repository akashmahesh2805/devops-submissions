# Exercise 10 - Multi-Node Kubernetes Cluster with Multiple Applications and Replicasets

## Objective

This project demonstrates a small e-commerce-style deployment on a three-node Minikube cluster:

- **AppA - Product Catalog:** Flask API with two replicas.
- **AppB - Shopping Cart:** Flask API with three replicas.
- Kubernetes Deployments create the required ReplicaSets and pods.
- Required pod anti-affinity distributes replicas of the same application across different nodes.

The applications are intentionally simple and use in-memory data. No database, frontend, authentication, or external service is required.

## Architecture

```text
Minikube profile: devops-multinode

Node 1       Node 2       Node 3
  |            |            |
  |       Product pod  Product pod
  |       Shopping pod Shopping pod Shopping pod
```

The exact pod-to-node assignment is chosen by Kubernetes. The important result is that Product Catalog replicas use different nodes and Shopping Cart replicas use all three nodes when three nodes are available.

Both Deployments use:

```yaml
podAntiAffinity:
  requiredDuringSchedulingIgnoredDuringExecution:
    - topologyKey: "kubernetes.io/hostname"
```

All manifests explicitly use the `default` namespace. This keeps Deployment and Service configuration consistent.

## Technologies

- Python
- Flask
- Docker
- Kubernetes
- Minikube
- kubectl
- Git and GitHub

## Project Structure

```text
Exercise 10 - Minikube Multi-Node Multi-App Minikube Deployment/
|-- product_catalog.py
|-- shopping_cart.py
|-- Dockerfile.product
|-- Dockerfile.shopping
|-- product_catalog_deployment.yaml
|-- shopping_cart_deployment.yaml
|-- product_catalog_service.yaml
|-- shopping_cart_service.yaml
|-- README.md
`-- .gitignore
```

## Check My Environment

Open PowerShell and run:

```powershell
python --version
docker --version
kubectl version --client
minikube version
git --version
```

These commands check Python, Docker Desktop/Docker Engine, the kubectl client, Minikube, and Git respectively.

Windows installation options:

- **Python:** install from https://www.python.org/downloads/windows/. During installation, select **Add Python to PATH**.
- **Docker Desktop:** install from https://www.docker.com/products/docker-desktop/. Start Docker Desktop and wait until it reports that Docker is running.
- **kubectl:** install from https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/. Docker Desktop can also provide kubectl.
- **Minikube:** install from https://minikube.sigs.k8s.io/docs/start/ and select Windows with the Docker driver.
- **Git:** install from https://git-scm.com/download/win.

Python is useful for local testing, but the Kubernetes deployment runs Flask inside the Docker images. Docker Desktop, kubectl, Minikube, and Git are required for the full assignment workflow.

## Test the Flask Applications Locally (Optional)

From this folder, install Flask if needed and run one application at a time:

```powershell
python -m pip install Flask
python product_catalog.py
```

In another PowerShell window, test it with:

```powershell
Invoke-RestMethod http://127.0.0.1/products
```

Stop it with `Ctrl+C`. To test the cart instead, run `python shopping_cart.py` and use the cart commands in the Testing section. Port 80 may require an administrator terminal on Windows, so Docker testing is usually simpler.

## Docker

Build both images from this folder:

```powershell
docker build -t product-catalog:latest -f Dockerfile.product .
docker build -t shopping-cart:latest -f Dockerfile.shopping .
docker images
```

The Dockerfiles use Python slim images, install Flask, copy one Python file, expose port 80, and run Flask on `0.0.0.0:80`.

## Create the Three-Node Minikube Cluster

The normal Windows/Docker Desktop command is:

```powershell
minikube start --nodes 3 --driver=docker -p devops-multinode
```

If an old profile is causing problems, clean it up first:

```powershell
minikube stop -p devops-multinode
minikube delete -p devops-multinode
```

Then run the start command again. Do not add `--force` normally. Use it only when Minikube prints a specific message saying that the operation must be forced, and first read the warning because it can bypass a safety check.

Verify the cluster:

```powershell
minikube status -p devops-multinode
kubectl get nodes
```

You should see one control-plane node and two worker nodes, for three nodes total. Node names may vary.

## Load Images into Minikube

Because this is a multi-node cluster, load both images into the Minikube profile:

```powershell
minikube -p devops-multinode image load product-catalog:latest
minikube -p devops-multinode image load shopping-cart:latest
```

The manifests use `imagePullPolicy: Never`, which tells Kubernetes to use the image already loaded into Minikube instead of trying to download it from Docker Hub. If you rebuild an image, run the matching `image load` command again.

## Kubernetes Deployment

Apply the Deployments first, then the Services:

```powershell
kubectl apply -f product_catalog_deployment.yaml
kubectl apply -f shopping_cart_deployment.yaml
kubectl apply -f product_catalog_service.yaml
kubectl apply -f shopping_cart_service.yaml
```

Useful verification commands:

```powershell
kubectl get deployments
kubectl get replicasets
kubectl get pods
kubectl get pods -o wide
kubectl get services
```

Expected Deployment readiness:

```text
product-catalog   2/2
shopping-cart    3/3
```

`kubectl get pods -o wide` includes the `NODE` column. Product Catalog pods must have different node names. The three Shopping Cart pods should have three different node names. Kubernetes generates the pod names, so do not expect fixed names.

## Access Services

Minikube opens each NodePort service and prints the actual local URL and port:

```powershell
minikube -p devops-multinode service product-catalog-service
minikube -p devops-multinode service shopping-cart-service
```

The port will not necessarily match a professor's example. Keep the printed URL, such as `http://127.0.0.1:xxxxx`, for the API tests. The command may open a browser automatically. `minikube service` also works from PowerShell or CMD. In WSL, use the printed address from Minikube and check Docker Desktop networking if localhost forwarding is unavailable.

## Testing

### Product Catalog

Replace `<PRODUCT_PORT>` with the port printed by the Product Catalog service command:

```powershell
curl.exe http://127.0.0.1:<PRODUCT_PORT>/products
```

PowerShell equivalent:

```powershell
Invoke-RestMethod http://127.0.0.1:<PRODUCT_PORT>/products
```

The response contains Laptop, Phone, and Headphones.

### Shopping Cart

Replace `<CART_PORT>` with the port printed by the Shopping Cart service command:

```powershell
curl.exe http://127.0.0.1:<CART_PORT>/cart
curl.exe -X POST http://127.0.0.1:<CART_PORT>/cart -H "Content-Type: application/json" -d "{\"id\":1,\"name\":\"Laptop\",\"quantity\":1}"
curl.exe http://127.0.0.1:<CART_PORT>/cart
```

The first GET returns `[]`. The POST returns HTTP 201 and the updated cart. The second GET returns the item. Because the cart is an in-memory list, each pod has its own cart and the data is not persistent. That is intentional for this assignment.

PowerShell equivalent:

```powershell
Invoke-RestMethod http://127.0.0.1:<CART_PORT>/cart
$body = @{ id = 1; name = 'Laptop'; quantity = 1 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:<CART_PORT>/cart -ContentType 'application/json' -Body $body
Invoke-RestMethod http://127.0.0.1:<CART_PORT>/cart
```

Use `curl.exe` in PowerShell because `curl` can be an alias for `Invoke-WebRequest` on some Windows versions.

## Troubleshooting

### Docker, Minikube, kubectl, or Git is not installed

Run the commands in **Check My Environment**, install only the missing tool using its official Windows link, restart PowerShell, and run the check again. Docker Desktop must be running before Minikube uses the Docker driver.

### Minikube will not start

Run:

```powershell
minikube version
minikube status -p devops-multinode
minikube logs -p devops-multinode
```

Confirm Docker Desktop is running, then clean up and recreate the profile with the commands in **Create the Three-Node Minikube Cluster**. If Docker reports insufficient CPU or memory, close other containers/apps or increase Docker Desktop resources.

### Pods show ImagePullBackOff or ErrImageNeverPull

The image is not available inside the Minikube profile, or the name does not match the manifest. Check:

```powershell
docker images
minikube -p devops-multinode image ls | Select-String 'product-catalog|shopping-cart'
```

Rebuild and load the exact image names:

```powershell
docker build -t product-catalog:latest -f Dockerfile.product .
docker build -t shopping-cart:latest -f Dockerfile.shopping .
minikube -p devops-multinode image load product-catalog:latest
minikube -p devops-multinode image load shopping-cart:latest
kubectl rollout restart deployment product-catalog
kubectl rollout restart deployment shopping-cart
```

### Pods are Pending

Inspect the pod and scheduler message:

```powershell
kubectl get pods -o wide
kubectl describe pod <pod-name>
```

Required anti-affinity prevents replicas of the same app from sharing a node. A three-replica Shopping Cart Deployment needs three schedulable nodes. Confirm with `kubectl get nodes`. Do not reduce the replica count for the assignment; fix the cluster node/resource issue instead.

### A Service does not open

Check selectors, endpoints, and service details:

```powershell
kubectl get services
kubectl get endpoints product-catalog-service shopping-cart-service
kubectl describe service product-catalog-service
kubectl describe service shopping-cart-service
```

Confirm the corresponding pods are Running and Ready, then rerun the correct `minikube -p devops-multinode service ...` command.

### A Flask container crashes

Find the pod name and inspect its logs:

```powershell
kubectl get pods
kubectl logs <pod-name>
```

Also check the pod events with `kubectl describe pod <pod-name>`. The applications must listen on `0.0.0.0` and port 80, as provided in the files.

## GitHub

Create an empty GitHub repository, then run these commands from this folder:

```powershell
git init
git add .
git commit -m "feat: add multi-node minikube deployment"
git branch -M main
git remote add origin <MY_GITHUB_REPOSITORY_URL>
git push -u origin main
```

Replace `<MY_GITHUB_REPOSITORY_URL>` with your actual repository URL, for example `https://github.com/your-username/your-repository.git`. Do not use the example URL unchanged. Open the repository on GitHub to verify that all files are present. The **Commits** page shows the commit message, author, and timestamp.

## Assignment Evidence Checklist

Capture these screenshots from your own successfully running machine. Do not create or fake output:

1. `minikube status -p devops-multinode`
2. `kubectl get nodes` showing three nodes
3. `docker images` showing both application images
4. `kubectl get deployments` showing `product-catalog 2/2` and `shopping-cart 3/3`
5. `kubectl get pods -o wide` showing replicas distributed across nodes
6. `kubectl get services`
7. Product Catalog `/products` response
8. Shopping Cart GET, POST, and updated GET response
9. GitHub repository file list
10. GitHub Commits page showing the commit and timestamp

## DO THIS IN ORDER

1. Run the five commands in **Check My Environment**.
2. Install only missing tools from the official links.
3. Open PowerShell in this `Assignment 2 - Minikube` folder.
4. Confirm the ten project files exist.
5. Optionally run one Flask app locally, then stop it with `Ctrl+C`.
6. Build `product-catalog:latest` with `Dockerfile.product`.
7. Build `shopping-cart:latest` with `Dockerfile.shopping`.
8. Run `docker images` and confirm both images exist.
9. Start Docker Desktop and create the `devops-multinode` three-node Minikube cluster.
10. Load both images with `minikube -p devops-multinode image load`.
11. Apply both Deployment manifests.
12. Apply both Service manifests.
13. Run `kubectl get nodes` and confirm three nodes.
14. Run `kubectl get deployments` and wait for `2/2` and `3/3`.
15. Run `kubectl get replicasets` to show ReplicaSets created by the Deployments.
16. Run `kubectl get pods -o wide` and verify different node names in the `NODE` column.
17. Open Product Catalog with `minikube -p devops-multinode service product-catalog-service`.
18. Open Shopping Cart with `minikube -p devops-multinode service shopping-cart-service`.
19. Test Product Catalog GET `/products`.
20. Test Shopping Cart GET `/cart`.
21. Test Shopping Cart POST `/cart`, then GET again.
22. Capture the ten evidence screenshots listed above.
23. Run `git init` and `git add .`.
24. Commit with `git commit -m "feat: add multi-node minikube deployment"`.
25. Create an empty GitHub repository.
26. Add your real repository URL with `git remote add origin ...`.
27. Push with `git push -u origin main`.
28. Open GitHub and verify the files and commit timestamp.
