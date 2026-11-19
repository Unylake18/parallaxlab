#!/bin/bash
cd "$(dirname "$0")"
for g in "PH PA PT1" "PT2 PT3 PT4" "PT5 PT6 PS"; do
  for C in $g; do ./medir.sh $C > /dev/null 2>&1 & done
  wait
done
ls medicao_*.json
