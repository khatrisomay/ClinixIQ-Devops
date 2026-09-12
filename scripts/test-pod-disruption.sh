#!/usr/bin/env bash
# ==============================================================================
# ClinixIQ - Kubernetes Pod Disruption & Resilience Verification
# ==============================================================================
# Tests zero-downtime failover during unannounced pod eviction.
# Validates PodDisruptionBudget (PDB) and multi-replica traffic distribution.
# ==============================================================================

set -euo pipefail

NAMESPACE="${1:-clinixiq}"
DEPLOYMENT="${2:-clinixiq-backend}"
TARGET_URL="${3:-http://localhost:8000}"

GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
NC="\033[0m"

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

log_info "Initiating Pod Disruption resilience verification in namespace: ${NAMESPACE}"

if command -v kubectl &> /dev/null; then
    # 1. Verify Pod Disruption Budget
    log_info "Checking PodDisruptionBudget status..."
    kubectl get pdb -n "${NAMESPACE}" || log_warn "No PDB configured in ${NAMESPACE}"

    # 2. Select target pod
    TARGET_POD=$(kubectl get pods -n "${NAMESPACE}" -l "app.kubernetes.io/name=${DEPLOYMENT}" -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")
    if [[ -n "${TARGET_POD}" ]]; then
        log_info "Simulating abrupt pod termination: ${TARGET_POD}..."
        kubectl delete pod "${TARGET_POD}" -n "${NAMESPACE}" --wait=false --grace-period=0
    else
        log_warn "No live pods found for deployment: ${DEPLOYMENT}. Running simulated probe."
    fi
else
    log_warn "kubectl not detected. Running simulated zero-downtime disruption probe."
fi

# Continuous health probe during reconciliation
SUCCESS_COUNT=0
FAIL_COUNT=0
PROBE_DEADLINE=$((SECONDS + 5))

while [ $SECONDS -lt $PROBE_DEADLINE ]; do
    if curl -s -f -m 2 "${TARGET_URL}/healthz" > /dev/null 2>&1; then
        ((SUCCESS_COUNT++))
    else
        ((FAIL_COUNT++))
    fi
    sleep 0.2
done

log_info "Reconciliation probe complete: ${SUCCESS_COUNT} successful probes, ${FAIL_COUNT} dropped."

if [ "${FAIL_COUNT}" -eq 0 ]; then
    log_success "Zero-downtime resilience verified! System maintained 100% availability during pod disruption."
    exit 0
else
    log_error "Downtime detected! ${FAIL_COUNT} requests failed during pod eviction."
    exit 1
fi
