#!/bin/bash
# stills de teste do T3 (handoff v6 §2.5), 1920×1080 → renders/stills_v6/: explosão, estroboscópio, split no contato, conta;
# e a prova da régua que corre (dois quadros a 0,5 s na faixa de baixo). Instantes em segundos do lote PT3.
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"; export PYTHONIOENCODING=utf-8
mkdir -p renders/stills_v6
m() { MEDIA_DIR="$PWD/media_still6_$3" STILL=$1 "$PY" -m manim -r 1920,1080 --fps 15 --progress_bar none -s cena.py PT3 > log_still6_$3.txt 2>&1
      cp "$(ls -t $(find media_still6_$3 -name "PT3_*.png") | head -1)" renders/stills_v6/$2; }
( m 15.33 T3-1_explosao_inicio.png a ) &
( m 22.5 T3-1_estrobo.png b ) &
( m 37.8 T3-3_split.png c ) &
wait
( m 55.2 T3-4_conta.png d ) &
( m 35.6 T3-3_regua_t0.png e ) &
( m 36.13 T3-3_regua_t0+0.5s.png f ) &
wait
ls renders/stills_v6
