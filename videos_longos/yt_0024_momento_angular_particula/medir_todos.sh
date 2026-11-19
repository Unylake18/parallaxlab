#!/bin/bash
cd "$(dirname "$0")"
for g in "PH PB1 PB2 PB3" "PB4 PB5 PB6 PS"; do
  for C in $g; do ./medir.sh $C > /dev/null 2>&1 & done
  wait
done
ls medicao_*.json
for C in PH PB1 PB2 PB3 PB4 PB5 PB6 PS; do echo "== $C: $(grep -c Traceback log_med_$C.txt) tracebacks"; done
