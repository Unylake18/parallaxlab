#!/bin/bash
# yt_0045 (copiado do yt_0043 ← yt_0041). Lote com fundo 3D: ./render3d.sh Classe
#   1) passagem seca (PEDIDOS3D=1) → threejs/pedidos3d/<Classe>.json (estado 3D de cada quadro)
#   2) node threejs/r3d.js → threejs/q3d/<Classe>_960x540/<cena>/fNNNNN.png (+ pontos.json para o QA de alinhamento)
#   3) render normal do Manim (./render.sh), que cola os PNGs atrás da camada Manim
cd "$(dirname "$0")"
PY="K:/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
export PYTHONUNBUFFERED=1
export CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"
C=$1; shift
T0=$(date +%s)
mkdir -p "media_$C/Tex"
cp -n media_*/Tex/*.svg "media_$C/Tex/" 2>/dev/null || true
SO_AUDITORIA=1 PEDIDOS3D=1 MEDIA_DIR="$PWD/media_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --dry_run --disable_caching cena.py $C > "log_ped_$C.txt" 2>&1
grep "\[3d\]\|Error\|error" "log_ped_$C.txt" | tail -3
rm -rf "threejs/q3d/${C}_960x540"
(cd threejs && NODE_PATH="K:/PycharmProjects/manim-fisica/videos_longos/yt_0020_cinematica_angular/threejs/node_modules" node r3d.js --lote $C) > "log_3d_$C.txt" 2>&1
tail -1 "log_3d_$C.txt"
echo "[3d] $C $(( $(date +%s) - T0 ))s" > "tempo3d_$C.txt"
./render.sh $C "$@"
