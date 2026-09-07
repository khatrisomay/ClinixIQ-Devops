#!/usr/bin/env bash
set -euo pipefail

echo "==> Stopping ClinixIQ compose stack..."
docker compose down -v --remove-orphans

if [ "${1:-}" == "--all" ]; then
    echo "==> Purging containers & dangling images..."
    docker image prune -f
fi

echo "==> Stack cleaned."
