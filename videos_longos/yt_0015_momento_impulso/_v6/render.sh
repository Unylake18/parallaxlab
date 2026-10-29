#!/bin/bash
# uso: ./render.sh Classe [ -- extra ]  → media_<Classe>/videos/cena/540p15/<Classe>.mp4 (preview 960×540 / 15 fps)
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
C=$1; shift
MEDIA_DIR="$PWD/media_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none "$@" cena.py $C > "log_$C.txt" 2>&1
tail -3 "log_$C.txt"
