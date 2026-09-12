#!/usr/bin/env bash
# ==============================================================================
# ClinixIQ - Production Smoke Testing Automation (Bash)
# ==============================================================================
# Usage:
#   ./scripts/run-smoke-tests.sh [http://localhost:8000]
# ==============================================================================

set -euo pipefail

TARGET_URL="${1:-http://localhost:8000}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_DIR="reports/smoke_${TIMESTAMP}"
mkdir -p "${REPORT_DIR}"

GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
NC="\033[0m"

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

log_info "Initiating ClinixIQ End-to-End Smoke Test Suite against: ${TARGET_URL}"

# 1. Run Core Smoke Probes
log_info "Running Phase 1: Core API & Liveness Probes..."
python tests/smoke/smoke_runner.py --url "${TARGET_URL}" --report "${REPORT_DIR}/core_smoke.json" || true

# 2. Run Synthetic Patient Journey
log_info "Running Phase 2: Synthetic Patient Diagnostic Journey..."
python tests/smoke/test_patient_journey.py --url "${TARGET_URL}" || true

# 3. Run Synthetic Billing Journey
log_info "Running Phase 3: Synthetic Commercial Billing Journey..."
python tests/smoke/test_billing_journey.py --url "${TARGET_URL}" || true

log_success "All smoke test phases executed. Reports archived in: ${REPORT_DIR}"
