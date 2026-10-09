#!/usr/bin/env bash
# Fetches only DBMS/OS/Networking-Interview-Questions from
# avinash201199/Interviews-Resources into data/raw/interviews-resources.
set -euo pipefail

DEST="data/raw/interviews-resources"
REPO_URL="https://github.com/avinash201199/Interviews-Resources.git"

rm -rf "$DEST"
git clone --depth 1 --filter=blob:none --sparse "$REPO_URL" "$DEST"
git -C "$DEST" sparse-checkout set --no-cone \
  "/DBMS-Interview-Questions/*" \
  "/OS-Interview-Questions/*" \
  "/Networking-Interview-Questions/*"

echo "Fetched into $DEST:"
find "$DEST" -name "*.pdf" | sort
