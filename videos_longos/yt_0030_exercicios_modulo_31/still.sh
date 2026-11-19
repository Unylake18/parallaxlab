#!/bin/bash
# yt_0026 (copiado do yt_0022): quadro parado de um lote no instante t (s do lote), para conferir layout. uso: ./still.sh PX5 35.0 → renders/still/PX5_35.0.png
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
C=$1; T=$2
mkdir -p renders/still
STILL=$T MEDIA_DIR="$PWD/media_still_${C}_$T" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --disable_caching -s cena.py $C > "renders/still/log_${C}_$T.txt" 2>&1
f=$(ls media_still_${C}_$T/images/cena/*.png 2>/dev/null | head -1); [ -n "$f" ] && cp "$f" "renders/still/${C}_$T.png" && rm -rf media_still_${C}_$T
echo "${C} $T $( [ -f renders/still/${C}_$T.png ] && echo ok || tail -2 renders/still/log_${C}_$T.txt)"
