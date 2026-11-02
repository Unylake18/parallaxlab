#!/bin/bash
# yt_0018 render FINAL (1920×1080 / 30 fps) de um lote: 3D (pedidos a 30 fps → Three.js 1920×1080) e Manim; sem auditoria (o QA foi feito no preview).
# uso: ./render_f1080.sh PX3   → media_F_<C>/videos/cena/1080p30/<C>.mp4
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8 FPS_RENDER=30
C=$1
TRES="PH PX2 PX3 PEP"
if [[ " $TRES " == *" $C "* ]]; then
  PEDIDOS3D=1 SO_AUDITORIA=1 MEDIA_DIR="$PWD/media_Fped_$C" "$PY" -m manim -r 1920,1080 --fps 30 --progress_bar none --dry_run cena.py $C > "log_Fped_$C.txt" 2>&1
  grep -E "Traceback|Error" "log_Fped_$C.txt" | head -3
  (cd threejs && CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe" node r3d.js --lote $C --w 1920 --h 1080) > "log_F3d_$C.txt" 2>&1
  tail -1 "log_F3d_$C.txt"
fi
AUDITORIA=0 MEDIA_DIR="$PWD/media_F_$C" "$PY" -m manim -r 1920,1080 --fps 30 --progress_bar none --disable_caching cena.py $C > "log_F_$C.txt" 2>&1
echo "== $C"; grep -E "\[tempo\] total|Error|Traceback" "log_F_$C.txt" | tail -2
