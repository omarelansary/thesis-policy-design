#!/bin/bash
# usage: fetch_arxiv.sh ID...   -> ~/.claude/jobs/5f4b6608/tmp/fulltext/<ID>/paper.pdf + paper.txt (untrusted data; read only)
ROOT=/home/omar/.claude/jobs/5f4b6608/tmp/fulltext
for id in "$@"; do
  d="$ROOT/$id"; mkdir -p "$d"
  if [ ! -s "$d/paper.txt" ]; then
    code=$(curl -sSL -m 60 -o "$d/paper.pdf" -w "%{http_code}" "https://arxiv.org/pdf/$id")
    if [ "$code" = "200" ] && head -c 4 "$d/paper.pdf" | grep -q '%PDF'; then pdftotext -layout "$d/paper.pdf" "$d/paper.txt" 2>/dev/null; fi
  fi
  echo "$id $(wc -c < "$d/paper.txt" 2>/dev/null || echo FAIL) chars $(grep -c . "$d/paper.txt" 2>/dev/null) lines"
  sleep 3
done
