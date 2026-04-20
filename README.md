# Kubernetes MediaWiki Deployment (Final Year Project)

This repository contains the Kubernetes manifests used to deploy a scalable **MediaWiki** application, including database, storage, monitoring, and testing configurations.

---

## 📌 Prerequisites

Before deploying, ensure you have:

* A working Kubernetes cluster
* Networking configured (CNI plugin installed)
* `kubectl` installed and configured
* Access to worker nodes
* Metrics Server support (required for HPA)

---

## 📁 Project Structure

```
Final-Year-Project/
├── database/
│   ├── mariadb-deployment.yaml
│   └── mariadb-service.yaml
├── mediawiki/
│   ├── mediawiki-deployment.yaml
│   └── mediawiki-service.yaml
├── storage/
│   ├── nfs-pv.yaml
│   ├── nfs-pvc.yaml
│   └── nfs-test-pod.yaml
├── testing/
│   ├── nginx-deployment.yaml
│   └── nginx-service.yaml
├── monitoring/
│   └── metrics-server.yaml
└── README.md
```

---

## 🚀 Deployment Steps (Order Matters)

### 🟢 1. Storage Configuration

Create persistent storage for the database:

```bash
kubectl apply -f storage/nfs-pv.yaml
kubectl apply -f storage/nfs-pvc.yaml
kubectl apply -f storage/nfs-test-pod.yaml
```

---

### 🟢 2. Database Deployment (MariaDB)

Deploy the database backend:

```bash
kubectl apply -f database/mariadb-deployment.yaml
kubectl apply -f database/mariadb-service.yaml
```

Verify:

```bash
kubectl get pods
kubectl get svc
```

---

### 🟢 3. MediaWiki Deployment

Deploy the MediaWiki application:

```bash
kubectl apply -f mediawiki/mediawiki-deployment.yaml
kubectl apply -f mediawiki/mediawiki-service.yaml
```

---

### 🟢 4. Monitoring Setup (Metrics Server)

Required for autoscaling:

```bash
kubectl apply -f monitoring/metrics-server.yaml
```

Verify:

```bash
kubectl top nodes
kubectl top pods
```

---

### 🟢 5. Testing Deployment (Optional)

Used for validating networking and load testing:

```bash
kubectl apply -f testing/nginx-deployment.yaml
kubectl apply -f testing/nginx-service.yaml
```

---

## 📈 Horizontal Pod Autoscaling (HPA)

Enable autoscaling for MediaWiki:

```bash
kubectl autoscale deployment mediawiki \
  --cpu-percent=50 \
  --min=2 \
  --max=5
```

Monitor scaling:

```bash
kubectl get hpa -w
```

---

## 🧪 Load Testing

Load testing was conducted using **Locust**, simulating multiple concurrent users interacting with the MediaWiki service.

---

## 📊 Features Demonstrated

* Kubernetes container orchestration
* Horizontal Pod Autoscaling (HPA)
* Persistent storage using NFS
* Monitoring via Metrics Server
* Load testing using Locust

---

## ⚠️ Notes

This deployment was tested in a **local virtualised environment**, meaning:

* Limited CPU and RAM resources
* Performance degradation under high load is expected
* Results may differ significantly in cloud environments

---

## 🔮 Future Improvements

* Deploy in a **cloud environment (AWS / Azure / GCP)**
* Implement **Pod Anti-Affinity** for better workload distribution
* Separate the **database onto a dedicated node**
* Increase available **CPU and memory resources**
* Implement **cluster autoscaling**
* Use more advanced **distributed storage solutions**

---

## 👨‍💻 Author

Final Year Project – Kubernetes-based MediaWiki Deployment
