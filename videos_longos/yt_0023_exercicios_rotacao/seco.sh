#!/bin/bash
# v2: passada seca (PEDIDOS3D=1) de um lote para pegar erros e medir as âncoras. uso: ./seco.sh LOTE → log_ped_LOTE.txt + resumo
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
C=$1
PEDIDOS3D=1 MEDIA_DIR="$PWD/media_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --dry_run cena.py $C > "log_ped_$C.txt" 2>&1
echo "== $C"
grep -a "^Exception\|Error:\|^\w*Error\|\[tempo\]\|FORA\|\[3d\]" "log_ped_$C.txt" | head -30
grep -a "\[gatilho\]" "log_ped_$C.txt" | tail -1
