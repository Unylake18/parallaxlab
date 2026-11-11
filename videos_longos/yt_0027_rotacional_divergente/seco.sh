#!/bin/bash
# final: passagem seca (sem render) que grava o plano de sincronia qa/plano/<C>.json. uso: ./seco.sh PHA PB1 ...
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
for C in "$@"; do SYNC_PLANO=gravar MEDIA_DIR="$PWD/media_seco_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --dry_run --disable_caching cena.py $C > "qa/log_seco_$C.txt" 2>&1 & done
wait
for C in "$@"; do echo "$C $(grep -h '\[sync\] plano\|Error' qa/log_seco_$C.txt | tail -1)"; done
