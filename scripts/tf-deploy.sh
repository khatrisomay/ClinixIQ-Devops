#!/usr/bin/env bash
# ==============================================================================
# ClinixIQ - Terraform Deployment Lifecycle Automation (Bash)
# ==============================================================================
# Usage:
#   ./scripts/tf-deploy.sh [init|validate|plan|apply|destroy] [dev|prod]
# ==============================================================================

set -euo pipefail

ACTION="${1:-validate}"
ENV="${2:-dev}"
TF_DIR="terraform"
VAR_FILE="environments/${ENV}/terraform.tfvars"
PLAN_FILE="tfplan-${ENV}.binary"

GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
NC="\033[0m"

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

if [[ ! -d "${TF_DIR}" ]]; then
    log_error "Terraform directory '${TF_DIR}' not found."
    exit 1
fi

case "${ACTION}" in
    init)
        log_info "Initializing Terraform modules and local backend..."
        terraform -chdir="${TF_DIR}" init -backend=false
        log_success "Terraform initialization complete."
        ;;
    validate)
        log_info "Verifying HCL formatting and syntax validation..."
        terraform fmt -check -recursive "${TF_DIR}"
        terraform -chdir="${TF_DIR}" init -backend=false
        terraform -chdir="${TF_DIR}" validate
        log_success "Terraform configuration is valid."
        ;;
    plan)
        log_info "Generating speculative execution plan for [${ENV}]..."
        terraform -chdir="${TF_DIR}" plan -var-file="${VAR_FILE}" -out="${PLAN_FILE}"
        log_success "Plan generated: ${TF_DIR}/${PLAN_FILE}"
        ;;
    apply)
        log_info "Applying execution plan for [${ENV}]..."
        if [[ ! -f "${TF_DIR}/${PLAN_FILE}" ]]; then
            log_warn "Saved plan not found. Generating fresh plan..."
            terraform -chdir="${TF_DIR}" plan -var-file="${VAR_FILE}" -out="${PLAN_FILE}"
        fi
        terraform -chdir="${TF_DIR}" apply "${PLAN_FILE}"
        rm -f "${TF_DIR}/${PLAN_FILE}"
        log_success "Terraform apply completed for [${ENV}]."
        ;;
    destroy)
        log_warn "DESTRUCTION WARNING: You are requesting destruction of [${ENV}] infrastructure!"
        read -p "Type the environment name '${ENV}' to confirm destruction: " CONFIRM
        if [[ "${CONFIRM}" == "${ENV}" ]]; then
            terraform -chdir="${TF_DIR}" destroy -var-file="${VAR_FILE}"
            log_success "Infrastructure destroyed."
        else
            log_error "Confirmation failed. Aborting."
            exit 1
        fi
        ;;
    *)
        echo "Usage: $0 {init|validate|plan|apply|destroy} [dev|prod]"
        exit 1
        ;;
esac
