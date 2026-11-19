#!/bin/bash
# yt_0021 v9: passe a seco (SYNC=medir) de um lote → medicao_<lote>.json (tempo nominal de animação/espera por trecho entre marcas)
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8 CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"
C=$1
SYNC=medir AUDITORIA=0 MEDIA_DIR="$PWD/media_med_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --disable_caching --dry_run cena.py $C > "log_med_$C.txt" 2>&1
tail -2 "log_med_$C.txt"
