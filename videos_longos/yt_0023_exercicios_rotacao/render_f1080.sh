#!/bin/bash
# yt_0023 render FINAL (1920×1080 / 30 fps) de um lote: 3D (pedidos a 30 fps → Three.js 1920×1080) e Manim; sem auditoria.
# uso: ./render_f1080.sh PE3   → media_F_<C>/videos/cena/1080p30/<C>.mp4
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8 FPS_RENDER=30 CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe" NODE_PATH="$(cd ../yt_0022_torque/threejs && pwd)/node_modules"
C=$1
s0=$(date +%s)
PEDIDOS3D=1 MEDIA_DIR="$PWD/media_Fped_$C" "$PY" -m manim -r 1920,1080 --fps 30 --progress_bar none --dry_run cena.py $C > "log_Fped_$C.txt" 2>&1
grep -E "Traceback|Error" "log_Fped_$C.txt" | head -3
rm -rf "threejs/q3d/${C}_1920x1080"
s1=$(date +%s)
(cd threejs && node r3d.js --lote $C --w 1920 --h 1080) > "log_F3d_$C.txt" 2>&1
tail -1 "log_F3d_$C.txt"
s2=$(date +%s)
AUDITORIA=0 MEDIA_DIR="$PWD/media_F_$C" "$PY" -m manim -r 1920,1080 --fps 30 --progress_bar none --disable_caching cena.py $C > "log_F_$C.txt" 2>&1
s3=$(date +%s)
echo "== $C pedidos=$((s1-s0))s 3d=$((s2-s1))s render=$((s3-s2))s"; grep -E "Error|Traceback" "log_F_$C.txt" | tail -2
echo "$C pedidos=$((s1-s0)) 3d=$((s2-s1)) render=$((s3-s2))" > "renders/_tempo_F_$C.txt"
