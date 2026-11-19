#!/bin/bash
# v2: onda de até 3 lotes: render3d (passada seca + Three.js + Manim) → auditoria → prancha. uso: ./onda_v2.sh PH PE1a PE1b
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
um() {
  L=$1
  ./render3d.sh $L > /dev/null 2>&1
  ./auditar.sh $L > /dev/null 2>&1
  "$PY" pr23.py $L 40 > /dev/null 2>&1
  echo "== $L: $(tail -1 log_3d_$L.txt 2>/dev/null | cut -c1-120)"
  grep -a "\[tempo\] total\|^Exception\|Error:\|FORA DA MARGEM\|FORA DA ZONA" log_$L.txt | head -6
}
for L in "$@"; do um $L & done
wait
echo ONDA_FIM
