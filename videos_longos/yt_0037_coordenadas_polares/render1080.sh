#!/bin/bash
# yt_0034 final (copiado do render1080.sh do yt_0032, com o 3D do render3d.sh): render FINAL 1920×1080 @ 30 fps de um lote (CRF 14 pelo
# template/qualidade.py; nada a configurar). Lotes com 3D: passada seca a 30 fps → pedidos → r3d.js em 1920×1080 → render.
# uso: ./render1080.sh Classe   Saída: media1080_<C>/videos/cena/1080p30/<C>.mp4, log1080_<C>.txt (e tempo3d1080_<C>.txt)
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8 FPS_RENDER=30
export CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"
C=$1
case " PH PB4 PB6 " in
  *" $C "*)
    T0=$(date +%s)
    PEDIDOS3D=1 MEDIA_DIR="$PWD/media1080_ped_$C" "$PY" -m manim -r 1920,1080 --fps 30 --progress_bar none --dry_run --disable_caching cena.py $C > "log1080_ped_$C.txt" 2>&1
    rm -rf "threejs/q3d/${C}_1920x1080"
    (cd threejs && NODE_PATH="$(cd ../../yt_0020_cinematica_angular/threejs/node_modules && pwd)" node r3d.js --lote $C --w 1920 --h 1080) > "log1080_3d_$C.txt" 2>&1
    echo "[3d1080] $C $(( $(date +%s) - T0 ))s $(tail -1 log1080_3d_$C.txt)" > "tempo3d1080_$C.txt"
    ;;
esac
T0=$(date +%s)
MEDIA_DIR="$PWD/media1080_$C" "$PY" -m manim -r 1920,1080 --fps 30 --progress_bar none --disable_caching cena.py $C > "log1080_$C.txt" 2>&1
echo "[render1080] $C $(( $(date +%s) - T0 ))s" >> "log1080_$C.txt"
tail -2 "log1080_$C.txt"
