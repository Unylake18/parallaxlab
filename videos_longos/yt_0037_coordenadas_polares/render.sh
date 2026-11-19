#!/bin/bash
# yt_0037 (copiado do yt_0032). uso: ./render.sh Classe [ -- extra ] → media_<Classe>/videos/cena/540p15/<Classe>.mp4 (preview 960×540 / 15 fps), log_<Classe>.txt.
# Sem cache do Manim (o 3D muda por PNG).
cd "$(dirname "$0")"
PY="K:/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
C=$1; shift
T0=$(date +%s)
MEDIA_DIR="$PWD/media_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --disable_caching "$@" cena.py $C > "log_$C.txt" 2>&1
echo "[render] $C $(( $(date +%s) - T0 ))s" >> "log_$C.txt"
tail -2 "log_$C.txt"
