#!/usr/bin/env bash
# Fetches only the files we need from donnemartin/system-design-primer into
# data/raw/system-design-primer: the main README (topic explanations) and the
# system_design solution write-ups. Skips images/, translated READMEs, and
# object_oriented_design (those are Jupyter notebooks/code, not prose — OOP
# content comes from a separate repo per CLAUDE.md).
set -euo pipefail

DEST="data/raw/system-design-primer"
REPO_URL="https://github.com/donnemartin/system-design-primer.git"

rm -rf "$DEST"
git clone --depth 1 --filter=blob:none --sparse "$REPO_URL" "$DEST"
git -C "$DEST" sparse-checkout set --no-cone \
  "/README.md" \
  "/solutions/system_design/*/README.md"

echo "Fetched into $DEST:"
find "$DEST" -name "*.md" | sort
