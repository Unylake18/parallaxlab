#!/bin/bash
# papel v2 (2026-11-11): render FINAL 1920×1080 @ 30 fps só do Manim (os quadros 3D 1080p já estão em threejs/q3d, refeitos com o c7.js atual
# e conferidos pelo qa3d_1080.py). uso: ./render1080_v2.sh PT PB1 ...  → media1080_<C>/videos/cena/1080p30/<C>.mp4, log1080_<C>.txt
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8 FPS_RENDER=30
for C in "$@"; do
  rm -rf "media1080_$C"
  AUDITORIA=0 MEDIA_DIR="$PWD/media1080_$C" "$PY" -m manim -r 1920,1080 --fps 30 --progress_bar none --disable_caching cena.py $C > "log1080_$C.txt" 2>&1
  echo "$C $(tail -1 log1080_$C.txt | cut -c1-120)"
done
