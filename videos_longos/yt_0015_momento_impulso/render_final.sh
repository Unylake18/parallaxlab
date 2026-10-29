#!/bin/bash
# render final 1920×1080 / 30 fps (sincronia da voz): ./render_final.sh Classe [-- extra]  → media_<Classe>/videos/cena/1080p30/
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8 SYNC=1
C=$1; shift
MEDIA_DIR="$PWD/media_$C" "$PY" -m manim -r 1920,1080 --fps 30 --progress_bar none "$@" cena.py $C > "logf_$C.txt" 2>&1
tail -1 "logf_$C.txt"
