#!/bin/bash
# prints 1920×1080 da rodada v6.1 → renders/stills_v6_1/: E4-2 (dois retângulos + MODELO), E4-4 (trabalho negativo), E4-6 (ícones)
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"; export PYTHONIOENCODING=utf-8
mkdir -p renders/stills_v6_1
t() { "$PY" -c "import json,re;a=json.load(open('ancoras.json',encoding='utf-8'))['ancoras'];L=open('log_$1.txt',encoding='utf-8').read();t0=float(re.search(r'\[an\] $2 ([0-9.]+)',L).group(1));print(round(t0+$3*a['$2']['dur'],3))"; }
m() { MEDIA_DIR="$PWD/media_still61_$1_$4" STILL=$2 "$PY" -m manim -r 1920,1080 --fps 15 --progress_bar none -s cena.py $1 > log_still61_$1_$4.txt 2>&1
      cp "$(ls -t $(find media_still61_$1_$4 -name "$1_*.png") | head -1)" renders/stills_v6_1/$3; }
( m PG $(t PG E4-2 0.9) E4-2_retangulos.png a ) &
( m PG $(t PG E4-4 0.92) E4-4_trabalho_negativo.png b ) &
( m PG $(t PG E4-6 0.95) E4-6_icones.png c ) &
wait
ls renders/stills_v6_1
