#!/bin/bash
# uso: _render_final.sh NOME SEÇÕES   → renders/final/NOME (1920×1080, 30 fps, CRF 14, ritmo.json)
cd /c/Users/Pichau/PycharmProjects/manim-fisica
D=videos_longos/yt_0006_magnetostatica_biot_savart; R=$D/renders/final/$1
rm -rf $R; mkdir -p $R; cp -r $D/renders/f1/Tex $R/Tex
S=$(date +%s)
SEG="$2" SYNC=$PWD/$D/ritmo.json CRF=14 PYTHONIOENCODING=utf-8 uv run --no-sync python -m manim -r 1920,1080 --fps 30 --disable_caching --media_dir $R $D/cena.py YT0006BiotSavart > $D/renders/final/$1.log 2>&1
echo "$1 exit $? em $(( $(date +%s) - S )) s" >> $D/renders/final/resultado.log
