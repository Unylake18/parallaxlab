#!/bin/bash
# Lote com fundo 3D: ./render3d.sh Classe
#   1) passagem seca (PEDIDOS3D=1) → threejs/pedidos3d/<Classe>.json (estado 3D de cada quadro)
#   2) node threejs/r3d.js → threejs/q3d/<Classe>_960x540/<cena>/fNNNNN.png (+ pontos.json para o QA de alinhamento)
#   3) render normal do Manim (./render.sh), que cola os PNGs atrás da camada Manim
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
export NODE_PATH="$(cd ../yt_0015_momento_impulso/threejs/node_modules && pwd -W 2>/dev/null || pwd)"
export CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"
C=$1; shift
PEDIDOS3D=1 MEDIA_DIR="$PWD/media_ped_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --dry_run cena.py $C > "log_ped_$C.txt" 2>&1
grep "\[3d\]\|Error\|error" "log_ped_$C.txt" | tail -3
rm -rf "threejs/q3d/${C}_960x540"
(cd threejs && node r3d.js --lote $C) > "log_3d_$C.txt" 2>&1
tail -1 "log_3d_$C.txt"
./render.sh $C "$@"
