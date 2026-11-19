#!/bin/bash
cd "$(dirname "$0")"
export RODADA=v4
for C in "$@"; do
  ./render3d.sh $C > /dev/null 2>&1
  if grep -q "Traceback" "log_$C.txt"; then echo "FALHA $C"; else echo "ok $C $(tail -n 1 log_$C.txt)"; fi
done
cd . && ../../.venv/Scripts/python.exe -X utf8 montar.py v4 2>&1 | tail -n 1
../../.venv/Scripts/python.exe -X utf8 qa41.py > log_qa_v3.txt 2>&1; echo FIM_V3B
