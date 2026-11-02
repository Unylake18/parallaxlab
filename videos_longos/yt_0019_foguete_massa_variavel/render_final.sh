#!/bin/bash
# yt_0019 v9: render FINAL 1920×1080 / 30 fps de um lote (3D: pedidos → Three.js 1080p → Manim). uso: ./render_final.sh PT2   → media_f_<Lote>/videos/cena/1080p30/<Lote>.mp4
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
C=$1
TRES="PH PT2 PT3 PT4 PE2 PS"
if [[ " $TRES " == *" $C "* ]]; then
  ./seco.sh $C > /dev/null
  rm -rf "threejs/q3d/${C}_1920x1080"
  (cd threejs && CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe" node r3d.js --lote $C --w 1920 --h 1080) > "log_3d_f_$C.txt" 2>&1
fi
rm -rf "media_f_$C"
AUDITORIA=0 MEDIA_DIR="$PWD/media_f_$C" "$PY" -m manim -r 1920,1080 --fps 30 --progress_bar none --disable_caching cena.py $C > "log_f_$C.txt" 2>&1
echo "== $C $(grep -E '\[tempo\] total|Error' log_f_$C.txt | tail -1)"
