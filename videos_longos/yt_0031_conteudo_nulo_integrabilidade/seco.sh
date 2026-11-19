#!/bin/bash
# yt_0031: passagem seca de um lote (sem vídeo) → log_seco_<Classe>.txt, para o ritmo por trecho (ritmo31.py).
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
C=$1
R5=0 MEDIA_DIR="$PWD/media_seco_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --dry_run --disable_caching cena.py $C > "log_seco_$C.txt" 2>&1
rm -rf "media_seco_$C"
