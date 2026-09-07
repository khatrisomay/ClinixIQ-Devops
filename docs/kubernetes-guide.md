# ClinixIQ Kubernetes & Helm Orchestration Architecture

## ☸️ Production Kubernetes Architecture

ClinixIQ is structured following strict CNCF enterprise standards:

```
                            [ Ingress Controller (Nginx + TLS) ]
                                          │
                   ┌──────────────────────┴──────────────────────┐
                   │ /                                           │ /api
                   ▼                                             ▼
       ┌──────────────────────┐                      ┌──────────────────────┐
       │ clinixiq-frontend    │                      │ clinixiq-backend     │
       │ (ClusterIP :8080)    │                      │ (ClusterIP :8000)    │
       │ Replicas: 2          │                      │ Replicas: 2-10 (HPA) │
       └──────────────────────┘                      └──────────┬───────────┘
                                                                │
                                                                ▼
                                                    ┌──────────────────────┐
                                                    │ clinixiq-redis       │
                                                    │ (ClusterIP :6379)    │
                                                    └──────────────────────┘
```

---

## 📂 Directory Structure

- `k8s/base/`: Base Kubernetes manifests (Deployments, Services, ConfigMaps, Secrets, RBAC, NetworkPolicies, HPA, PDB).
- `k8s/overlays/dev/`: Developer overlay (1 replica, debug logging).
- `k8s/overlays/prod/`: Production overlay (HA 3 replicas, production domain routing).
- `helm/clinixiq/`: Production Helm 3 chart for parameterized releases.

---

## 🛠️ Deployment Instructions

### Method 1: Kustomize Multi-Environment Deployment
```bash
# Validate manifests via dry-run
kubectl apply -k k8s/overlays/dev --dry-run=client

# Deploy to Dev Environment
kubectl apply -k k8s/overlays/dev

# Deploy to Production Environment
kubectl apply -k k8s/overlays/prod
```

### Method 2: Helm Chart Deployment
```bash
# Dry-run template rendering
helm template clinixiq ./helm/clinixiq

# Deploy release
helm upgrade --install clinixiq ./helm/clinixiq \
  --namespace clinixiq \
  --create-namespace
```
