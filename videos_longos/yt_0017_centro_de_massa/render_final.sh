#!/bin/bash
# Render final de um lote: 1920×1080 / 30 fps (CRF 14 automático pelo template, ≥ 1080p).
#   1) passada seca (PEDIDOS3D=1) a 540p30 no media_<Classe> do preview → threejs/pedidos3d/<Classe>.json (os pedidos só dependem do fps;
#      o cache de LaTeX do preview evita recompilar tudo — um MEDIA_DIR novo recompila cada fórmula)
#   2) node threejs/r3d.js --lote <Classe> --w 1920 --h 1080 (só se o lote tiver 3D)
#   3) Manim 1920×1080 / 30 fps → media_final_<Classe>/videos/cena/1080p30/<Classe>.mp4 (log em log_final_<Classe>.txt)
# uso: ./render_final.sh Classe
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
export CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"
C=$1; shift
PEDIDOS3D=1 MEDIA_DIR="$PWD/media_$C" "$PY" -m manim -r 960,540 --fps 30 --progress_bar none --dry_run cena.py $C > "log_ped_final_$C.txt" 2>&1
grep "\[3d\]\|Error" "log_ped_final_$C.txt" | tail -3
grep -q "\[tempo\]" "log_ped_final_$C.txt" || { echo "passada seca falhou"; exit 1; }
if grep -q "\[3d\] pedidos:" "log_ped_final_$C.txt"; then
  rm -rf "threejs/q3d/${C}_1920x1080"
  (cd threejs && node r3d.js --lote $C --w 1920 --h 1080) > "log_3d_final_$C.txt" 2>&1
  tail -1 "log_3d_final_$C.txt"
fi
mkdir -p "media_final_$C" && cp -rn "media_$C/Tex" "media_final_$C/" 2>/dev/null
MEDIA_DIR="$PWD/media_final_$C" "$PY" -m manim -r 1920,1080 --fps 30 --progress_bar none --disable_caching "$@" cena.py $C > "log_final_$C.txt" 2>&1
tail -3 "log_final_$C.txt"
