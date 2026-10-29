#!/bin/bash
# stills 1920×1080 do v6 (handoff v6 §5.8) → renders/stills_v6/: além dos 4 do T3 (stills_v6_t3.sh), T1-6 (barras), E1 (Δp⃗ em três
# linhas), E2 (∦), E3 (foguete fora do gráfico), E4 (miniaturas), T6 (K = p²/2m em três linhas), E5 (2 mg (miligramas)).
# Instante = início da âncora (linhas [an] do log_<lote>.txt) + fração da fala; o still interpola o play no instante exato (kit v6).
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"; export PYTHONIOENCODING=utf-8
mkdir -p renders/stills_v6
t() { "$PY" -c "import json,re;a=json.load(open('ancoras.json',encoding='utf-8'))['ancoras'];L=open('log_$1.txt',encoding='utf-8').read();t0=float(re.search(r'\[an\] $2 ([0-9.]+)',L).group(1));print(round(t0+$3*a['$2']['dur'],3))"; }
m() { MEDIA_DIR="$PWD/media_still6_$1_$4" STILL=$2 "$PY" -m manim -r 1920,1080 --fps 15 --progress_bar none -s cena.py $1 > log_still6_$1_$4.txt 2>&1
      cp "$(ls -t $(find media_still6_$1_$4 -name "$1_*.png") | head -1)" renders/stills_v6/$3; }
( m PT1 $(t PT1 T1-6 0.85) T1-6_barras.png a ) &
( m PE $(t PE E1-2 0.75) E1_dp_tres_linhas.png a ) &
( m PE $(t PE E2-3 0.95) E2_nao_paralela.png b ) &
( m PE $(t PE E3-1 0.62) E3_foguete_fora.png c ) &
wait
( m PG $(t PG E4-3 0.8) E4_miniaturas.png a ) &
( m PF $(t PF T6-2 0.97) T6_K_tres_linhas.png a ) &
( m PG $(t PG E5-1 0.6) E5_miligramas.png b ) &
wait
ls renders/stills_v6
