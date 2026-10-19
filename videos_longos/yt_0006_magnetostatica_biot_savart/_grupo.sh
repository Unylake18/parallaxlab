#!/bin/bash
# uso: _grupo.sh NOME SEÇÕES  (render por trecho; Tex em cache copiado)
cd /c/Users/Pichau/PycharmProjects/manim-fisica
D=videos_longos/yt_0006_magnetostatica_biot_savart
SEG="$2" QA_STILLS=1 uv run python -m manim -r 960,540 --fps 15 --media_dir $D/renders/$1 $D/cena.py YT0006BiotSavart > $D/renders/$1/log.txt 2>&1
echo "$1 exit $?"
