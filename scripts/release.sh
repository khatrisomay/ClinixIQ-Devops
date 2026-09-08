#!/usr/bin/env bash
set -euo pipefail

VERSION="${1:-}"
MESSAGE="${2:-Release ${VERSION}}"

if [[ ! "${VERSION}" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "❌ Version must match format vX.Y.Z (e.g., v1.2.0)"
    exit 1
fi

echo "==> Creating Release Tag: ${VERSION}..."
git tag -a "${VERSION}" -m "${MESSAGE}"
echo "✅ Tag created. Run: git push origin ${VERSION}"
