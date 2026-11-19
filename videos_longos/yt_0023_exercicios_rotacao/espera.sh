#!/bin/bash
# espera até cada log citado ter "[tempo] total" ou Traceback; imprime o estado
cd "$(dirname "$0")"
while true; do
  pend=0
  for f in "$@"; do grep -aqs "\[tempo\] total\|Traceback" $f || pend=1; done
  [ $pend = 0 ] && break; sleep 20
done
for f in "$@"; do echo "== $f"; grep -a "\[tempo\] total" $f; grep -a -A40 "Traceback" $f | grep -a "Error\|\.py:[0-9]" | tail -6; done
