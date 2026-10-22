#!/usr/bin/env bash
# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE:
# MODULE:    Grand Public Production Launch & System Handover
# TOPIC:     Phase 141 SEO, 64-District OpenGraph Engine, Production CI/CD & National Handover
# FILE:      scripts/rollback.sh
# PHASE:     Phase 141 - Grand Public Production Launch & Final Handover
# PURPOSE:   Sub-30-second automated production rollback script with health check validation
# STANDARDS: Zero-Emoji, Zero-IDOR, Production Grade, WCAG 2.2 AAA, Full 64-District Support
# ==============================================================================

set -euo pipefail

TARGET_RELEASE="${1:-previous}"
APP_DIR="${APP_DIR:-/var/www/studentlifecircle}"
HEALTH_URL="${HEALTH_URL:-http://localhost:3000/}"

echo "[ROLLBACK INITIATED] Target release: ${TARGET_RELEASE} at $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Step 1: Locate previous verified standalone build or Git tag
if [ "${TARGET_RELEASE}" = "previous" ]; then
    echo "[INFO] Resolving previous verified deployment..."
    TARGET_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "HEAD~1")
else
    TARGET_TAG="${TARGET_RELEASE}"
fi

echo "[INFO] Rolling back code to: ${TARGET_TAG}"

# Step 2: Switch Git pointer or container tag
if command -v git >/dev/null 2>&1 && [ -d .git ]; then
    git checkout "${TARGET_TAG}"
fi

# Step 3: Fast asset synchronization
if [ -d "frontend/.next/standalone" ]; then
    cp -r frontend/public frontend/.next/standalone/ 2>/dev/null || true
    cp -r frontend/.next/static frontend/.next/standalone/.next/ 2>/dev/null || true
fi

# Step 4: Gracefully restart process / systemd service
if command -v systemctl >/dev/null 2>&1; then
    echo "[INFO] Restarting systemd service: studentlifecircle-frontend..."
    sudo systemctl restart studentlifecircle-frontend || true
fi

# Step 5: Immediate Health Check Assertion
echo "[INFO] Performing health assertion against ${HEALTH_URL}..."
for i in {1..10}; do
    STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${HEALTH_URL}" || echo "000")
    if [ "${STATUS_CODE}" -eq 200 ]; then
        echo "[SUCCESS] Rollback verified healthy! HTTP 200 received in attempt ${i}."
        exit 0
    fi
    echo "[WAIT] Attempt ${i}: Waiting for service response (status: ${STATUS_CODE})..."
    sleep 2
done

echo "[CRITICAL ALERT] Health check failed after rollback. Escalating to on-call engineer."
exit 1
