#!/bin/bash
cd "$(dirname "$0")"
for g in "PH PA PT1" "PT2 PT3 PT4" "PT5 PT6 PS"; do
  for C in $g; do ./auditar.sh $C > /dev/null 2>&1 & done
  wait
done
PY=../../.venv/Scripts/python.exe
$PY qa22.py > renders/qa_run.txt 2>&1; $PY agrupar_portao.py > /dev/null 2>&1; $PY classifica_portao.py 2>&1 | tail -1
