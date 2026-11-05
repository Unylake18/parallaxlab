#!/bin/bash
# yt_0020 (copiado do yt_0019): passada seca de pedidos 3D (sem desenhar quadros) → threejs/pedidos3d/<Classe>.json. uso: ./seco.sh Classe
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
C=$1
SO_AUDITORIA=1 PEDIDOS3D=1 MEDIA_DIR="$PWD/media_ped_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --disable_caching --dry_run cena.py $C > "log_ped_$C.txt" 2>&1
grep -E "\[3d\]|\[tempo\] total|Error" "log_ped_$C.txt" | tail -3
