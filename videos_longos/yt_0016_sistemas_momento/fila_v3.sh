#!/bin/bash
# fila de render do v3 (pedidos 3D já gravados pela passagem seca do seco_v3.sh): ./fila_v3.sh L1 L2 ...
#   lote com 3D: node r3d.js (quadros 960×540 + pontos.json) e depois o render do Manim; lote 2D: só o render.
cd "$(dirname "$0")"
export NODE_PATH="$(cd ../yt_0015_momento_impulso/threejs/node_modules && pwd -W 2>/dev/null || pwd)"
export CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"
for C in "$@"; do
  if [ -f "threejs/pedidos3d/$C.json" ] && grep -q '\[3d\]' "log_ped_$C.txt"; then
    rm -rf "threejs/q3d/${C}_960x540"
    (cd threejs && node r3d.js --lote $C) > "log_3d_$C.txt" 2>&1
    echo "$C 3d: $(tail -1 log_3d_$C.txt)"
  fi
  ./render.sh $C > /dev/null
  echo "$C: $(grep 'tempo\] total' log_$C.txt) $(grep -c Traceback log_$C.txt) erros"
done
