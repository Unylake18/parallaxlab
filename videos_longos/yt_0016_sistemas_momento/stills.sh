#!/bin/bash
# stills 1920×1080 do v1 → renders/stills_v1/: H1, T7-4, T8-5, T9-6, E7-5, E9-4.
# Instante = 0,4 s antes do início da âncora seguinte (lido do [ancora] em log_<lote>.txt do preview), ou o 4º argumento (s).
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"; export PYTHONIOENCODING=utf-8
mkdir -p renders/stills_v1
t_fim() { awk -v a="$2" '/\[ancora\]/{ if (f) { print $3 - 0.4; exit } if ($2 == a) f = 1 }' log_$1.txt; }
m() { local T; T=${4:-$(t_fim $1 $2)}; MEDIA_DIR="$PWD/media_still_$1" STILL=$T "$PY" -m manim -r 1920,1080 --fps 15 --progress_bar none -s cena.py $1 > log_still_$1.txt 2>&1
      cp "$(ls -t $(find media_still_$1 -name "$1_*.png") | head -1)" renders/stills_v1/$3; echo "$3 @ $T s"; }
( m PH H1 H1_cavalo_e_pedra.png ) &
( m P7 T7-4 T7-4_matriz_de_pares.png ) &
( m P8 T8-5 T8-5_setas_do_cavalo.png ) &
wait
( m P9 T9-6 T9-6_grafico_P.png ) &
( m Q7 E7-5 E7-5_barras_log.png 79.4 ) &
( m Q9 E9-4 E9-4_forma_de_snell.png ) &
wait
ls -la renders/stills_v1
