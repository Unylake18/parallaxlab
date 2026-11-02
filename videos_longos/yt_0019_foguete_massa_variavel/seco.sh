#!/bin/bash
# yt_0019 v3: passada seca rápida (sem desenhar, sem auditoria) para achar erro de código. Nos lotes 3D grava os pedidos (PEDIDOS3D=1).
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
C=$1
TRES="PH PT2 PT3 PT4 PE2 PS"
if [[ " $TRES " == *" $C "* ]]; then P=1; else P=0; fi
PEDIDOS3D=$P SO_AUDITORIA=1 MEDIA_DIR="$PWD/media_ped_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --dry_run cena.py $C > "log_ped_$C.txt" 2>&1
grep -E "\[tempo\] total|Error|\[3d\]" "log_ped_$C.txt" | tail -3
