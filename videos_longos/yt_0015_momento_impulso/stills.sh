#!/bin/bash
# stills 1920×1080 do v2 → renders/stills_v2/: H3 (os dois manequins), T1-4 (tabela), T5-4 (Riemann → integral),
# T6-1 (dois painéis), E4-4 (dois caminhos). Instantes = fim de cada âncora no lote (ver log_<lote>.txt).
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"; export PYTHONIOENCODING=utf-8
export CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"
mkdir -p renders/stills_v2
m() { MEDIA_DIR="$PWD/media_still_$1" STILL=$2 "$PY" -m manim -r 1920,1080 --fps 15 --progress_bar none -s "${@:3}" cena.py $1 > log_still_$1.txt 2>&1; }
p() { cp "$(ls -t $(find media_still_$1 -name "$1_*.png") | head -1)" renders/stills_v2/$2; }
( m PB 52.0 && p PB T1-4_tabela.png ) &
( m PD 65.0 && p PD T5-4_riemann_integral.png ) &
wait
( m PF 16.8 && p PF T6-1_dois_paineis.png ) &
( m PG 53.6 && p PG E4-4_dois_caminhos.png ) &
( cd threejs && node render3d.js --trecho hook --w 1920 --h 1080 --quadros 495 --out frames3d_still_hook > /dev/null 2>&1; cd .. && m PH 33.0 -t && "$PY" - <<'P'
from PIL import Image
import glob, os
bg = Image.open("threejs/frames3d_still_hook/f00495.png").convert("RGBA")
fg = Image.open(max(glob.glob("media_still_PH/images/cena/PH_*.png"), key=os.path.getmtime)).convert("RGBA")
Image.alpha_composite(bg, fg).convert("RGB").save("renders/stills_v2/H3_dois_manequins.png")
P
) &
wait
ls -la renders/stills_v2
