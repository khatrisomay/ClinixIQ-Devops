#!/usr/bin/env bash
set -euo pipefail

WEBHOOK_URL="${1:-}"
STATUS="${2:-SUCCESS}"
BUILD_NUM="${3:-local}"
BRANCH="${4:-main}"

if [ -z "${WEBHOOK_URL}" ]; then
    echo "⚠️ WEBHOOK_URL not provided. Skipping notification dispatch."
    exit 0
fi

echo "==> Sending ${STATUS} notification to webhook..."

PAYLOAD=$(cat <<EOF
{
  "text": "ClinixIQ CI/CD Status: *${STATUS}* | Build: #${BUILD_NUM} | Branch: ${BRANCH}"
}
EOF
)

curl -s -X POST -H 'Content-type: application/json' --data "${PAYLOAD}" "${WEBHOOK_URL}" || true
echo "✅ Notification processed."
