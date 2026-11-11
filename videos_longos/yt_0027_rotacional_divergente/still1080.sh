#!/bin/bash
# still 1920x1080 de um lote no instante t: ./still1080.sh PB2 49.5 → renders/v2/qa/still1080_PB2_49.5.png
cd "$(dirname "$0")"; PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"; export PYTHONIOENCODING=utf-8
QA=${QA:-renders/v2/qa}; mkdir -p $QA
STILL=$2 MEDIA_DIR="$PWD/media_s1080_$1_$2" "$PY" -m manim -r 1920,1080 --fps 15 --progress_bar none --disable_caching -s cena.py $1 > /dev/null 2>&1
f=$(ls media_s1080_$1_$2/images/cena/*.png | head -1); cp "$f" $QA/still1080_$1_$2.png; rm -rf media_s1080_$1_$2
