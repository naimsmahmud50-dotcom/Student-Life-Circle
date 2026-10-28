#!/usr/bin/env bash
# ========================================================================================
# AUTOMATED GITHUB PAGES DEPLOYMENT SCRIPT
# MODULE:    Static Site Export & gh-pages Branch Deployment
# STANDARDS: Strict Zero-Emoji Policy, Automated Error Trapping, Idempotent Execution
# ========================================================================================

set -e

echo "[PAGES DEPLOY] Starting GitHub Pages deployment pipeline..."

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"
OUT_DIR="$FRONTEND_DIR/out"

# Step 1: Execute static export build if out directory does not exist or build is requested
if [ ! -d "$OUT_DIR" ] || [ "$1" == "--rebuild" ]; then
  echo "[PAGES DEPLOY] Building static production export..."
  cd "$FRONTEND_DIR"
  NEXT_PUBLIC_BASE_PATH=/Student-Life-Circle NEXT_EXPORT=true npm run build
fi

# Step 2: Ensure .nojekyll guard exists in exported output
echo "[PAGES DEPLOY] Inoculating export with .nojekyll guard..."
touch "$OUT_DIR/.nojekyll"

# Step 3: Stage build artifacts in an isolated deployment directory
echo "[PAGES DEPLOY] Staging static artifacts in temporary directory..."
TEMP_DEPLOY_DIR=$(mktemp -d)
cp -r "$OUT_DIR/." "$TEMP_DEPLOY_DIR/"

cd "$TEMP_DEPLOY_DIR"
git init
git config user.name "$(git -C "$ROOT_DIR" config user.name || echo 'Mahmud Hasan')"
git config user.email "$(git -C "$ROOT_DIR" config user.email || echo 'mahmud@ogrojatra.edu.bd')"
git checkout -b gh-pages
git add -A
git commit -m "deploy: update live github pages static build $(date -u +'%Y-%m-%d %H:%M:%S UTC')"

# Step 4: Push to origin gh-pages
REMOTE_URL=$(git -C "$ROOT_DIR" config --get remote.origin.url)
echo "[PAGES DEPLOY] Pushing static assets to $REMOTE_URL (branch: gh-pages)..."
git remote add origin "$REMOTE_URL"
git push -f origin gh-pages

# Step 5: Clean up
echo "[PAGES DEPLOY] Cleaning up temporary staging environment..."
cd "$ROOT_DIR"
rm -rf "$TEMP_DEPLOY_DIR"

echo "[PAGES DEPLOY] GitHub Pages deployment completed successfully."
echo "[PAGES DEPLOY] Live Website: https://naimsmahmud50-dotcom.github.io/Student-Life-Circle/"
