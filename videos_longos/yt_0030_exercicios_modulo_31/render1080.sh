#!/bin/bash
# yt_0030 final (copiado do yt_0028): render FINAL 1920×1080 @ 30 fps de um lote, SEM PERDAS (CRF=0: fonte da costura; o vídeo final passa por uma
# única compressão em CRF 14 no montar1080.py). uso: ./render1080.sh Classe  → media1080_<C>/videos/cena/1080p30/<C>.mp4, log1080_<C>.txt
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8 FPS_RENDER=30 CRF=${CRF:-0}
C=$1
AUDITORIA=0 MEDIA_DIR="$PWD/media1080_$C" "$PY" -m manim -r 1920,1080 --fps 30 --progress_bar none --disable_caching cena.py $C > "log1080_$C.txt" 2>&1
tail -2 "log1080_$C.txt"
