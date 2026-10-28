#!/bin/bash
# stills 1920×1080: C01-4 (3D+setas), C05-4 (triângulo), C07-3 (as duas áreas), C13-3 (refração 3D+ângulos) → renders/stills/
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"; export PYTHONIOENCODING=utf-8
export CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"
mkdir -p renders/stills
m() { MEDIA_DIR="$PWD/media_still_$1" STILL=$2 "$PY" -m manim -r 1920,1080 --fps 15 --progress_bar none -s "${@:3}" cena.py $1 > log_still_$1.txt 2>&1; }
( m PB 141.6 && cp $(find media_still_PB -name "PB_*.png" | head -1) renders/stills/C05-4_triangulo.png ) &
( m PC 43.3 && cp $(find media_still_PC -name "PC_*.png" | head -1) renders/stills/C07-3_duas_areas.png ) &
( cd threejs && node render3d.js --trecho c01 --w 1920 --h 1080 --quadros 735 --out frames3d_still_c01 > /dev/null 2>&1; cd .. && m PT1 49.0 -t && "$PY" - <<'P'
from PIL import Image
import glob
bg = Image.open("threejs/frames3d_still_c01/f00735.png").convert("RGBA")
fg = Image.open(glob.glob("media_still_PT1/images/cena/PT1_*.png")[0]).convert("RGBA")
Image.alpha_composite(bg, fg).convert("RGB").save("renders/stills/C01-4_visao_do_carro_3d.png")
P
) &
( cd threejs && node render3d.js --trecho c13 --w 1920 --h 1080 --quadros 450 --out frames3d_still_c13 > /dev/null 2>&1; cd .. && m PT2 30.0 -t && "$PY" - <<'P'
from PIL import Image
import glob
bg = Image.open("threejs/frames3d_still_c13/f00450.png").convert("RGBA")
fg = Image.open(glob.glob("media_still_PT2/images/cena/PT2_*.png")[0]).convert("RGBA")
Image.alpha_composite(bg, fg).convert("RGB").save("renders/stills/C13-3_refracao_3d.png")
P
) &
wait
ls -la renders/stills
