#!/bin/bash
# yt_0044 final §6: passada seca PRESSA=grava de um lote → renders/pressa/<LOTE>.json (fator de cada trecho entre gatilhos). uso: ./pressa.sh LOTE
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
C=$1
rm -f "renders/pressa/$C.json"
PRESSA=grava MEDIA_DIR="$PWD/media_pressa_$C" timeout 1800 "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --dry_run --disable_caching cena.py $C > "log_pressa_$C.txt" 2>&1
echo "$C $(grep -h '\[pressa\]' log_pressa_$C.txt) $(grep -l Traceback log_pressa_$C.txt >/dev/null && echo ERRO)"
