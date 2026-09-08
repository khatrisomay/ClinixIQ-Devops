#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${1:-clinixiq}"
ENDPOINT_URL="${2:-http://localhost:8000/healthz}"
TIMEOUT_SEC="${3:-90}"

echo "==> Verifying Kubernetes Rollout in namespace '${NAMESPACE}'..."

if kubectl rollout status deployment/clinixiq-backend -n "${NAMESPACE}" --timeout="${TIMEOUT_SEC}s" && \
   kubectl rollout status deployment/clinixiq-frontend -n "${NAMESPACE}" --timeout="${TIMEOUT_SEC}s"; then
    echo "-> Rollout status successful. Performing healthcheck..."
    if curl -sf "${ENDPOINT_URL}" > /dev/null; then
        echo "✅ Deployment verified: Pods healthy and traffic responsive."
        exit 0
    fi
fi

echo "❌ Deployment verification failed! Triggering automatic rollback..."
kubectl rollout undo deployment/clinixiq-backend -n "${NAMESPACE}"
kubectl rollout undo deployment/clinixiq-frontend -n "${NAMESPACE}"
echo "⚠️ Rollback triggered."
exit 1
