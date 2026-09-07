.PHONY: help build up down logs restart test clean k8s-apply k8s-delete

SHELL := /bin/bash
TAG ?= latest

help:
	@echo "ClinixIQ DevOps Platform - Make Automation"
	@echo "=========================================="
	@echo "  make build         - Build all multi-stage Docker images"
	@echo "  make up            - Launch local Docker Compose stack"
	@echo "  make down          - Tear down Docker Compose stack"
	@echo "  make restart       - Restart Docker Compose stack"
	@echo "  make logs          - Tail container logs"
	@echo "  make test          - Run backend and integration tests"
	@echo "  make test-backend  - Run backend pytest suite"
	@echo "  make k8s-dry-run   - Dry-run validate Kubernetes base manifests"
	@echo "  make clean         - Remove containers and temporary files"

build:
	@echo "==> Building container images..."
	docker compose build

up:
	@echo "==> Launching ClinixIQ Compose Stack..."
	docker compose up -d
	@echo "Frontend running at: http://localhost:3000"
	@echo "Backend API running at: http://localhost:8000/docs"

down:
	@echo "==> Stopping ClinixIQ Stack..."
	docker compose down -v --remove-orphans

restart: down up

logs:
	docker compose logs -f

test: test-backend

test-backend:
	@echo "==> Executing Backend Pytest Suite..."
	cd backend && python -m pytest -v tests/

k8s-dry-run:
	@echo "==> Validating Kubernetes manifests..."
	kubectl apply --dry-run=client -k k8s/base

clean:
	@echo "==> Cleaning cache and dangling resources..."
	docker compose down -v --remove-orphans
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
