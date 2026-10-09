#!/usr/bin/env bash
# Fetches the single README.md from Devinterview-io/oop-interview-questions
# (the whole repo is just this one file) into data/raw/oop-interview-questions/.
set -euo pipefail

DEST_DIR="data/raw/oop-interview-questions"
mkdir -p "$DEST_DIR"
curl -sf https://raw.githubusercontent.com/Devinterview-io/oop-interview-questions/main/README.md \
  -o "$DEST_DIR/README.md"

echo "Fetched $DEST_DIR/README.md ($(wc -l < "$DEST_DIR/README.md") lines)"
