#!/bin/bash
# stills 1920×1080 do v5 → renders/stills_v5/ (handoff v5 §3.5): T1-2 (lupa), T1-3, T1-5 (caixa), T1-6 (barras), carros, T4 (Δp⃗ nos
# discos), E2, T6 (luvas), E5 (dois caminhos), F2 (corda). Instante = início da âncora (linhas [an] do log_<lote>.txt) + fração da fala.
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"; export PYTHONIOENCODING=utf-8
export CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"
mkdir -p renders/stills_v5
t() { "$PY" -c "import json,re;a=json.load(open('ancoras.json',encoding='utf-8'))['ancoras'];L=open('log_$1.txt',encoding='utf-8').read();t0=float(re.search(r'\[an\] $2 ([0-9.]+)',L).group(1));print(round(t0+$3*a['$2']['dur'],3))"; }
m() { MEDIA_DIR="$PWD/media_still5_$1_$4" STILL=$2 "$PY" -m manim -r 1920,1080 --fps 15 --progress_bar none -s cena.py $1 > log_still5_$1_$4.txt 2>&1
      cp "$(ls -t $(find media_still5_$1_$4 -name "$1_*.png") | head -1)" renders/stills_v5/$3; }
( m PT1 $(t PT1 T1-2 0.3) T1-2_lupa.png a ) &
( m PT1 $(t PT1 T1-3 0.9) T1-3_p_igual_mv.png b ) &
( m PT1 $(t PT1 T1-5 0.93) T1-5_caixa.png c ) &
wait
( m PT1 $(t PT1 T1-6 0.85) T1-6_barras.png d ) &
( m PT1 $(t PT1 T1-4 0.8) T1-4_carros.png e ) &
( m PC $(t PC T4-1 0.75) T4_dp_nos_discos.png a ) &
wait
( m PE $(t PE E2-3 0.85) E2_triangulo.png a ) &
( m PF $(t PF T6-3 0.85) T6_luvas.png a ) &
( m PG $(t PG E5-3 0.85) E5_dois_caminhos.png a ) &
wait
# F2: 3D em 1920×1080 + camada Manim transparente
( cd threejs && node render3d.js --trecho cavalo --w 1920 --h 1080 --quadros 200 --out frames3d_still5_cavalo > /dev/null 2>&1 )
MEDIA_DIR="$PWD/media_still5_PF2" STILL=13.333 "$PY" -m manim -r 1920,1080 --fps 15 --progress_bar none -s -t cena.py PF2 > log_still5_PF2.txt 2>&1
"$PY" - <<'P'
import glob, os
from PIL import Image
bg = Image.open("threejs/frames3d_still5_cavalo/f00200.png").convert("RGBA")
fg = Image.open(max(glob.glob("media_still5_PF2/images/cena/PF2_*.png"), key=os.path.getmtime)).convert("RGBA")
Image.alpha_composite(bg, fg).convert("RGB").save("renders/stills_v5/F2_corda.png")
P
ls -la renders/stills_v5
