#!/bin/bash
cd /c/Users/Pichau/PycharmProjects/manim-fisica
D=videos_longos/yt_0006_magnetostatica_biot_savart; R=$D/renders
rm -rf $R/ev; mkdir -p $R/ev; cp -r $R/f1/Tex $R/ev/Tex; rm -f $R/eventos.jsonl
SEG=nenhuma QA_EVENTS=$R/eventos.jsonl uv run python -m manim -r 960,540 --fps 15 --media_dir $R/ev $D/cena.py YT0006BiotSavart > $R/ev/log.txt 2>&1
echo "ev exit $?" > $R/eventos_done.txt
