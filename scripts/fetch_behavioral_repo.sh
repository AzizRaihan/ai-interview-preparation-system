#!/usr/bin/env bash
# Fetches only the behavioral-interview*.md content pages from
# yangshun/tech-interview-handbook (a Docusaurus monorepo now, not a plain
# markdown-questions repo) into data/raw/tech-interview-handbook.
set -euo pipefail

DEST="data/raw/tech-interview-handbook"
REPO_URL="https://github.com/yangshun/tech-interview-handbook.git"

rm -rf "$DEST"
git clone --depth 1 --filter=blob:none --sparse "$REPO_URL" "$DEST"
git -C "$DEST" sparse-checkout set --no-cone \
  "/apps/website/contents/behavioral-interview*.md"

echo "Fetched into $DEST:"
find "$DEST" -name "behavioral-interview*.md" | sort
