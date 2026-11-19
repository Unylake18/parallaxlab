#!/bin/bash
# yt_0045 (copiado do yt_0043 ← yt_0041): quadro parado de um lote no instante t (s do lote). uso: ./still.sh PH 35.0 → renders/still/PH_35.0.png
cd "$(dirname "$0")"
PY="K:/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
C=$1; T=$2
mkdir -p renders/still "media_still_${C}_$T/Tex"
cp -n "media_$C/Tex/"*.svg "media_still_${C}_$T/Tex/" 2>/dev/null || true
if [ -f "threejs/pedidos3d/${C}.json" ]; then
  FQ=$("$PY" -c "print(int(round(float('$T')*15)))")
  (cd threejs && NODE_PATH="K:/PycharmProjects/manim-fisica/videos_longos/yt_0020_cinematica_angular/threejs/node_modules" CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe" node r3d.js --lote $C --w 1920 --h 1080 --so "$FQ,$((FQ-1)),$((FQ+1))") > /dev/null 2>&1 || true
fi
STILL=$T MEDIA_DIR="$PWD/media_still_${C}_$T" "$PY" -m manim -r 1920,1080 --fps 15 --progress_bar none --disable_caching -s cena.py $C > "renders/still/log_${C}_$T.txt" 2>&1
f=$(ls media_still_${C}_$T/images/cena/*.png 2>/dev/null | head -1); [ -n "$f" ] && cp "$f" "renders/still/${C}_$T.png" && rm -rf media_still_${C}_$T
echo "${C} $T $( [ -f renders/still/${C}_$T.png ] && echo ok || tail -2 renders/still/log_${C}_$T.txt)"
