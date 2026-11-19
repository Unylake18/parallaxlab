#!/bin/bash
# yt_0032 (copiado do yt_0031). Lote com fundo 3D: ./render3d.sh Classe
#   1) passagem seca (PEDIDOS3D=1) → threejs/pedidos3d/<Classe>.json (estado 3D de cada quadro)
#   2) node threejs/r3d.js → threejs/q3d/<Classe>_960x540/<cena>/fNNNNN.png (+ pontos.json para o QA de alinhamento)
#   3) render normal do Manim (./render.sh), que cola os PNGs atrás da camada Manim
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
export CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"
C=$1; shift
T0=$(date +%s)
PEDIDOS3D=1 MEDIA_DIR="$PWD/media_ped_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --dry_run --disable_caching cena.py $C > "log_ped_$C.txt" 2>&1
grep "\[3d\]\|Error\|error" "log_ped_$C.txt" | tail -3
rm -rf "threejs/q3d/${C}_960x540"
(cd threejs && NODE_PATH="$(cd ../../yt_0020_cinematica_angular/threejs/node_modules && pwd)" node r3d.js --lote $C) > "log_3d_$C.txt" 2>&1
tail -1 "log_3d_$C.txt"
echo "[3d] $C $(( $(date +%s) - T0 ))s" > "tempo3d_$C.txt"
./render.sh $C "$@"
