#!/bin/bash
# stills 1920×1080 do v3 → renders/stills_v3/: H3, T2 (vista lateral), E2 (triângulo), T6 (mãos), E4 (gráfico em escala real),
# E5 (zoom da pulga), F2 (cavalo). Instantes dos lotes 2D: início da âncora (audit_v3_<lote>.txt, linhas [an]) + deslocamento.
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"; export PYTHONIOENCODING=utf-8
export CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"
mkdir -p renders/stills_v3
t() { awk -v a="$2" '$2==a {print $3 + '"$3"'}' audit_v3_$1.txt; }
m() { MEDIA_DIR="$PWD/media_still_$1" STILL=$2 "$PY" -m manim -r 1920,1080 --fps 15 --progress_bar none -s "${@:3}" cena.py $1 > log_still_$1.txt 2>&1; }
p() { cp "$(ls -t $(find media_still_$1 -name "$1_*.png") | head -1)" renders/stills_v3/$2; }
comp() {  # trecho quadro classe instante saída
  ( cd threejs && node render3d.js --trecho $1 --w 1920 --h 1080 --quadros $2 --out frames3d_still_$1 > /dev/null 2>&1 )
  m $3 $4 -t
  "$PY" - "$1" "$2" "$3" "$5" <<'P'
import sys, glob, os
from PIL import Image
tr, q, cl, out = sys.argv[1:5]
bg = Image.open(f"threejs/frames3d_still_{tr}/f{int(q):05d}.png").convert("RGBA")
fg = Image.open(max(glob.glob(f"media_still_{cl}/images/cena/{cl}_*.png"), key=os.path.getmtime)).convert("RGBA")
Image.alpha_composite(bg, fg).convert("RGB").save(f"renders/stills_v3/{out}")
P
}
( m PE $(t PE E2-3 17.5) && p PE E2_triangulo.png ) &
( m PF $(t PF T6-3 27.0) && p PF T6_maos.png ) &
wait
( m PG $(t PG E4-2 14.0) && p PG E4_escala_real.png ) &
MEDIA_DIR="$PWD/media_still_PG5" STILL=$(t PG E5-1 15.5) "$PY" -m manim -r 1920,1080 --fps 15 --progress_bar none -s cena.py PG > log_still_PG5.txt 2>&1; cp "$(ls -t $(find media_still_PG5 -name "PG_*.png") | head -1)" renders/stills_v3/E5_zoom_pulga.png
wait
comp hook 495 PH 33.0 H3_dois_manequins.png
comp trilho 420 PT2 28.0 T2_vista_lateral.png
comp cavalo 200 PF2 13.333 F2_cavalo.png
ls -la renders/stills_v3
