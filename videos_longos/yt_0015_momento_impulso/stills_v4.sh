#!/bin/bash
# stills 1920×1080 do v4 → renders/stills_v4/ (handoff v4 §7): T1-2, T1-5, T1-6, T5-2, T5-6, T5-8, E4 (caminhos), E5 (caminhos).
# Instante = início da âncora (linhas [an] do log_<lote>.txt, render com ANCORAS=1) + fração da fala.
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"; export PYTHONIOENCODING=utf-8
mkdir -p renders/stills_v4
t() { "$PY" -c "import json,re,sys;a=json.load(open('ancoras.json',encoding='utf-8'))['ancoras'];L=open('log_$1.txt',encoding='utf-8').read();t0=float(re.search(r'\[an\] $2 ([0-9.]+)',L).group(1));print(round(t0+$3*a['$2']['dur'],3))"; }
m() { MEDIA_DIR="$PWD/media_still_$1_$4" STILL=$2 "$PY" -m manim -r 1920,1080 --fps 15 --progress_bar none -s cena.py $1 > log_still_$1_$4.txt 2>&1
      cp "$(ls -t $(find media_still_$1_$4 -name "$1_*.png") | head -1)" renders/stills_v4/$3; }
( m PT1 $(t PT1 T1-2 0.95) T1-2_m_na_derivada.png a ) &
( m PT1 $(t PT1 T1-5 0.93) T1-5_projecoes.png b ) &
( m PT1 $(t PT1 T1-6 0.8) T1-6_barras.png c ) &
wait
( m PD $(t PD T5-2 0.75) T5-2_triangulo_conta.png a ) &
( m PD $(t PD T5-6 0.62) T5-6_troca_limites.png b ) &
( m PD $(t PD T5-8 0.85) T5-8_componentes.png c ) &
wait
( m PG $(t PG E4-4 0.95) E4_caminhos.png a ) &
( m PG $(t PG E5-3 0.85) E5_pulga_caminhos.png b ) &
wait
ls -la renders/stills_v4
