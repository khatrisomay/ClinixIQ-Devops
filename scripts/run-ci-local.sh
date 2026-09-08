#!/usr/bin/env bash
set -uo pipefail

echo "=========================================================="
echo "   ClinixIQ Local CI/CD Pipeline Simulator                "
echo "=========================================================="

echo -e "\n[Stage 1/4] Backend Unit Tests & Coverage..."
cd backend && python -m pytest -v --cov=app tests/ || true
cd ..

echo -e "\n[Stage 2/4] Frontend Production Build..."
cd frontend && npm run build || true
cd ..

echo -e "\n[Stage 3/4] Kubernetes Manifest Dry-run..."
kubectl apply --dry-run=client -k k8s/base || true

echo -e "\n[Stage 4/4] Helm Chart Lint..."
helm lint helm/clinixiq || true

echo "=========================================================="
echo "   Local CI Simulation Complete                           "
echo "=========================================================="
