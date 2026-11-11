#!/bin/bash
# yt_0028 v3 (handoff v3 §9.2): still a 1920×1080 de um lote no instante t (s do lote), sem vídeo (-s). uso: ./still1080.sh PB1 71.93 03
# → renders/v3/qa/alinhamento/still1080_NN.png
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
C=$1; T=$2; N=$3
D=renders/v3/qa/alinhamento
mkdir -p $D
STILL=$T MEDIA_DIR="$PWD/media_s1080_${N}" "$PY" -m manim -r 1920,1080 --fps 15 --progress_bar none --disable_caching -s cena.py $C > "$D/log_still_${N}.txt" 2>&1
f=$(ls media_s1080_${N}/images/cena/*.png 2>/dev/null | head -1); [ -n "$f" ] && cp "$f" "$D/still1080_${N}.png" && rm -rf media_s1080_${N}
echo "$N $C $T $( [ -f $D/still1080_${N}.png ] && echo ok || tail -2 $D/log_still_${N}.txt)"
