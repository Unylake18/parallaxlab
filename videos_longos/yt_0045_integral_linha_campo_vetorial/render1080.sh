#!/bin/bash
# yt_0045 final (copiado do yt_0044; sem 3D: a lata é 2D): render FINAL 1920×1080 @ 30 fps de um lote (CRF 14 pelo
# template/qualidade.py; nada a configurar).
# uso: ./render1080.sh Classe   Saída: media1080_<C>/videos/cena/1080p30/<C>.mp4, log1080_<C>.txt (e tempo3d1080_<C>.txt)
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8 FPS_RENDER=30 RODADA=final
export CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"
C=$1
T0=$(date +%s)
MEDIA_DIR="$PWD/media1080_$C" "$PY" -m manim -r 1920,1080 --fps 30 --progress_bar none --disable_caching cena.py $C > "log1080_$C.txt" 2>&1
echo "[render1080] $C $(( $(date +%s) - T0 ))s" >> "log1080_$C.txt"
tail -2 "log1080_$C.txt"
