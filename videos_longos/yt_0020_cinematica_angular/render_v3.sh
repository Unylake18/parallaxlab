#!/bin/bash
# yt_0020 (copiado do yt_0019): um lote do começo ao fim. 3D: pedidos (passada seca) → Three.js (r3d.js) → render do Manim; em paralelo com o
# render, a passada só de auditoria (auditar.sh, a cada 3 quadros). uso: ./render_v3.sh PT5 [--sem3d]
cd "$(dirname "$0")"
C=$1
TRES="PH PT4 PT5 PE3 PS"
if [[ " $TRES " == *" $C "* && "$2" != "--sem3d" ]]; then
  ./seco.sh $C > /dev/null
  rm -rf "threejs/q3d/${C}_960x540"
  (cd threejs && CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe" node r3d.js --lote $C) > "log_3d_$C.txt" 2>&1
fi
./render.sh $C &
./auditar.sh $C &
wait
echo "== $C"; grep -E "\[tempo\] total|Error" log_$C.txt | tail -1; grep -E "\[tempo\] total|Error" log_aud_$C.txt | tail -1
