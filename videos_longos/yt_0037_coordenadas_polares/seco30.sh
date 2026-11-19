#!/bin/bash
# passada seca a 30 fps / 1080p (as auditorias R5 amostram diferente de 15 fps). uso: ./seco30.sh LOTE → log_seco30_LOTE.txt
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8 FPS_RENDER=30
MEDIA_DIR="$PWD/media_seco30_$1" "$PY" -m manim -r 1920,1080 --fps 30 --progress_bar none --dry_run --disable_caching cena.py $1 > "log_seco30_$1.txt" 2>&1
echo "$1 R5=$(grep -c '^\[R5\]' log_seco30_$1.txt)"; grep '^\[R5\]' log_seco30_$1.txt | cut -c1-200
