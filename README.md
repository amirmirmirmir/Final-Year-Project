# Final Year Project - Kubernetes MediaWiki Deployment

This repository contains the Kubernetes manifests, supporting configuration, and test scripts used for my Final Year Project.

The goal of the project was to deploy and evaluate a containerised MediaWiki application on a Kubernetes cluster, supported by:

- NFS-backed persistent storage
- MariaDB database integration
- Monitoring with Prometheus and Grafana
- Horizontal Pod Autoscaling (HPA)
- Load testing with Locust

## Important Assumption

This repository **does not** provision the Kubernetes cluster itself.

It is expected that you already have:

- A working Kubernetes cluster
- Networking correctly configured
- A Container Network Interface (CNI) installed
- Worker nodes joined and in a `Ready` state
- NFS server prepared and reachable from the cluster
- `kubectl` configured on the control plane
- `helm` installed for monitoring components

This repository focuses only on the **deployment code and configuration files** used once the cluster is already operational.

---

## Repository Contents

### Kubernetes Manifests
Located in `kubernetes/`

- **storage/**  
  PersistentVolume and PersistentVolumeClaim definitions for NFS-backed storage

- **database/**  
  MariaDB deployment and service definitions

- **mediawiki/**  
  MediaWiki deployment, service, and configuration integration

- **autoscaling/**  
  Horizontal Pod Autoscaler configuration

- **testing/**  
  Test workloads such as the Nginx validation deployment

### Monitoring Notes
Located in `monitoring/`

Contains the key commands and deployment notes for:

- Prometheus
- Grafana
- Metrics Server

### Load Testing
Located in `locust/`

Contains the Locust script used to simulate user traffic against the MediaWiki deployment.

---

## Deployment Order

The manifests should generally be applied in the following order:

### 1. Storage
```bash
kubectl apply -f kubernetes/storage/nfs-pv.yaml
kubectl apply -f kubernetes/storage/nfs-pvc.yaml
```

### 2. Database
```bash
kubectl apply -f kubernetes/database/mariadb-deployment.yaml
kubectl apply -f kubernetes/database/mariadb-service.yaml
```

### 3. MediaWiki
```bash
kubectl apply -f kubernetes/mediawiki/mediawiki-deployment.yaml
kubectl apply -f kubernetes/mediawiki/mediawiki-service.yaml
```

### 4. MediaWiki configuration
If using a ConfigMap for `LocalSettings.php`:

```bash
kubectl apply -f kubernetes/mediawiki/localsettings-configmap.yaml
kubectl rollout restart deployment mediawiki
```

### 5. Autoscaling
```bash
kubectl apply -f kubernetes/autoscaling/mediawiki-hpa.yaml
```

---

## Validation Commands

### Check pods
```bash
kubectl get pods -o wide
```

### Check services
```bash
kubectl get svc
```

### Check persistent volumes
```bash
kubectl get pv,pvc
```

### Check HPA
```bash
kubectl get hpa -w
```

---

## Monitoring Stack

Prometheus and Grafana were installed using Helm rather than raw YAML.

Typical setup flow:

### Add repositories
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

### Create monitoring namespace
```bash
kubectl create namespace monitoring
```

### Install Prometheus
```bash
helm install prometheus prometheus-community/prometheus \
  --namespace monitoring \
  --set server.persistentVolume.enabled=false \
  --set alertmanager.persistentVolume.enabled=false
```

### Install Grafana
```bash
helm install grafana grafana/grafana \
  --namespace monitoring \
  --set service.type=NodePort \
  --set service.nodePort=32090 \
  --set persistence.enabled=false
```

### Install Metrics Server
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

If required in a local lab environment, edit the Metrics Server deployment to include:

```yaml
--kubelet-insecure-tls
```

---

## Load Testing

The Locust test script is located in:

```text
locust/locustfile.py
```

Example usage:

```bash
locust -f locust/locustfile.py
```

Example test targets used in the project:

- 5 users, 1 user/sec ramp-up, 5 minutes
- 25 users, 1 user/sec ramp-up, 5 minutes
- 100 users, 2 users/sec ramp-up, 3 minutes

---

## Example Access URLs

### MediaWiki
```text
http://<node-ip>:32080
```

### Grafana
```text
http://<node-ip>:32090
```

### Prometheus
Usually accessed with port forwarding:
```bash
kubectl port-forward -n monitoring <prometheus-pod-name> 9090
```

---

## Notes

This repository reflects a **local Kubernetes lab environment** built for academic testing and evaluation.  
Some decisions, such as disabling persistence for Prometheus and Grafana or using `--kubelet-insecure-tls` for Metrics Server, were made specifically for local development constraints and would be handled differently in production.

---

## Author

Amir  
Final Year Project
