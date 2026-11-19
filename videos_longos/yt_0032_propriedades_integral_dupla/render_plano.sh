#!/bin/bash
# yt_0032: passada seca que grava o plano de ritmo (renders/plano/<LOTE>.json) e depois o render normal (2D ou 3D) já usando o plano.
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
for C in ${@:-PH PA PB1 PB2 PB3 PB4 PB5 PB6 PB7 PS}; do
  PLANO=grava MEDIA_DIR="$PWD/media_plano_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --dry_run --disable_caching cena.py $C > "log_plano_$C.txt" 2>&1
  grep "\[plano\]\|Error" "log_plano_$C.txt" | tail -2
  ./render_todos.sh $C
done
