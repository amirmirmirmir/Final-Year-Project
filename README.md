# Kubernetes MediaWiki Deployment (Final Year Project)

This repository contains the Kubernetes manifests used to deploy a scalable **MediaWiki** application, including database, storage, monitoring, and testing configurations.
Due to the nature of the project, this repository exists mostly to provide my Supervisor with a means to look at the YAML and Python files created for the project as implementing this in its entirety is known to be a huge task in itself

---

## Prerequisites

Before deploying, ensure you have:

* A working Kubernetes cluster set up with 4 components, 1 Master Node, 2 Worker Nodes and an NFS Server acting as storage
* Networking configured (CNI plugin installed)
* Minimum of 2 CPUs and 4GB of Ram per Node
* Replace yaml files where appropriate with your respective parameters, for example the NFS Server IP address in nfs-pv.yaml
* Ensure your cluster works if you haven't with the basic Nginx application deployment.


---

## Project Structure

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
│   └── locustfile.py

├── monitoring/
│   └── metrics-server.yaml
└── README.md
```

---

##  Deployment Steps in order

###  1. Storage Configuration

Create persistent storage for the database:

```bash
kubectl apply -f storage/nfs-pv.yaml
kubectl apply -f storage/nfs-pvc.yaml
kubectl apply -f storage/nfs-test-pod.yaml
```
Following the deployment of the nfs-test pod you should be able to Cat the file defined in it to verify if it worked correctly and then delete the deployment if you want. You will also need to update any relevant IP addresses with your own configurations

---

###  2. Database Deployment (MariaDB)

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

###  3. MediaWiki Deployment

Deploy the MediaWiki application:

```bash
kubectl apply -f mediawiki/mediawiki-deployment.yaml
kubectl apply -f mediawiki/mediawiki-service.yaml
```
Once MediaWiki is deployed, complete the setup for the application and create a ConfigMap using:

```bash
kubectl create configmap mediawiki-config --from-file=LocalSettings.php
```
Verify with:

```bash
kubectl get configmaps
```
Following this update the mediawiki-deployment.yaml file to ensure it fits your ConfigMap.
You should then be able to delete and repdeploy MediaWiki with data persistence.

---

###  4. Monitoring Setup (Metrics Server)

It is recommended here to install Prometheus and Grafana onto your own cluster through Helm using the appropriate installation for your device
For the scope of the infrastucture, it is also recommend to turn off persistentVolumes for the server and alertmanager for Prometheus and Grafana when creating the monitoring namespace 

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

##  Horizontal Pod Autoscaling (HPA)

Enable autoscaling for MediaWiki:

```bash
kubectl autoscale deployment mediawiki \
  --cpu-percent=50 \
  --min=2 \
  --max=5
```

Monitor scaling:

```bash
kubectl get pods -w
```

```bash
kubectl get hpa -w
```
If percentages do not have an actual value, for example if using VirtualBox as your virtualisation means, the Metrics-Server configuration should be modified to do so, however if you are using mine this should already be rectified in context to VirtualBox

---

##  Load Testing

Load testing can be conducted using the Locust file, install Locust on your host machine.
CD into the directory of the Locust file, run locust in the terminal and run tests directed towards the IP address of your deployed MediaWiki
If the monitoring stack was setup, this should provide you with test results for your cluster
---

##  Features Demonstrated

* Kubernetes container orchestration
* Horizontal Pod Autoscaling (HPA)
* Persistent storage using NFS
* Monitoring via Metrics Server
* Load testing using Locust

---

##  Notes

This deployment was tested in a **local virtualised environment**, meaning:

* Limited CPU and RAM resources
* Performance degradation under high load is expected
* Results may differ significantly in cloud environments

---

##  Future Improvements

* Deploy in a **cloud environment (AWS / Azure / GCP)**
* Implement **Pod Anti-Affinity** for better workload distribution
* Separate the **database onto a dedicated node**
* Increase available **CPU and memory resources**


---

Mohammad Bari - Final Year Project – Kubernetes-based MediaWiki Deployment
