# Changelog

All notable changes to the **ClinixIQ DevOps Platform** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-09-08
### Added
- Enterprise Jenkins multibranch declarative pipeline (`Jenkinsfile`) with 8 automated stages.
- GitHub Actions CI/CD matrix workflows for automated linting, test suites, and container publishing.
- Aqua Security Trivy container and filesystem vulnerability scanner.
- Gitleaks automated high-entropy secret detection.
- Zero-downtime deployment and automated rollback scripts (`verify-deployment.sh` / `.ps1`).
- Custom Jenkins controller Dockerfile with pre-installed DevOps CLI tools (`helm`, `kubectl`, `trivy`).
- Jenkins Configuration as Code (`casc.yaml`) and Docker Compose orchestrator.

## [1.1.0] - 2026-09-07
### Added
- Multi-container Docker Compose configuration with custom bridge network and healthchecks.
- Async Redis 7.2 caching and sub-millisecond query layer with rate limiting.
- Production Nginx reverse proxy gateway routing API and SPA endpoints.
- Complete CNCF-compliant Kubernetes manifests (Base, Kustomize `dev`/`prod` overlays).
- Horizontal Pod Autoscaler (HPA) and Pod Disruption Budgets (PDB).
- Zero-trust NetworkPolicies and Persistent Volume Claims.
- Production Helm 3 chart in `helm/clinixiq/`.

## [1.0.0] - 2026-09-03
### Added
- Interactive symptom triage assistant with differential diagnosis engine.
- FastAPI microservice with clinical NLP tokenization and disease prediction model.
- Dynamic headless Matplotlib vector SVG graph streaming.
- High-acuity medical design system, brand logo, and responsive dashboard.
- Multi-stage non-root Dockerfiles for frontend and backend.
