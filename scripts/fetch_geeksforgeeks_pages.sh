#!/usr/bin/env bash
# Fetches the 5 GeeksforGeeks interview-question pages used to supplement/replace
# the thin OOP/DBMS/OS/Networking/Behavioral sources. Plain curl works (verified:
# GfG serves full server-rendered HTML, no bot-block encountered).
set -euo pipefail

DEST="data/raw/geeksforgeeks"
mkdir -p "$DEST"

UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

NAMES=(oop dbms os networking behavioral)
URLS=(
  "https://www.geeksforgeeks.org/interview-prep/oops-interview-questions/"
  "https://www.geeksforgeeks.org/dbms/commonly-asked-dbms-interview-questions/"
  "https://www.geeksforgeeks.org/operating-systems/operating-systems-interview-questions/"
  "https://www.geeksforgeeks.org/top-50-computer-networking-interview-questions-and-answers/"
  "https://www.geeksforgeeks.org/hr/hr-interview-questions/"
)

for i in "${!NAMES[@]}"; do
  name="${NAMES[$i]}"
  curl -sL -A "$UA" "${URLS[$i]}" -o "$DEST/$name.html"
  size=$(wc -c < "$DEST/$name.html")
  echo "$name: $size bytes -> $DEST/$name.html"
done
