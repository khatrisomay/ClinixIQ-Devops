#!/usr/bin/env bash
set -euo pipefail

TAG="${1:-latest}"
echo "==> Building ClinixIQ Images with tag: $TAG..."

echo "-> Building Backend..."
docker build -t "clinixiq-backend:${TAG}" -f backend/Dockerfile ./backend

echo "-> Building Frontend..."
docker build -t "clinixiq-frontend:${TAG}" -f frontend/Dockerfile ./frontend

echo "-> Building Gateway..."
docker build -t "clinixiq-gateway:${TAG}" -f gateway/Dockerfile ./gateway

echo "==> Build complete."
docker images | grep "clinixiq" || true
