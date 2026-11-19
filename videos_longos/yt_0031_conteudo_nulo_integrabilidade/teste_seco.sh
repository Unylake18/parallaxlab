#!/bin/bash
# yt_0031 final: passada seca COM R5/embolado (sem vídeo) de vários lotes em paralelo → log_teste_<C>.txt. uso: ./teste_seco.sh PB7 PB4 ...
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
for C in "$@"; do
  (MEDIA_DIR="$PWD/media_teste_$C" timeout 1200 "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --dry_run --disable_caching cena.py $C > "log_teste_$C.txt" 2>&1; rm -rf "media_teste_$C"; echo "[fim] $C") &
done
wait
