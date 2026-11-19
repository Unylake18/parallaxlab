#!/bin/bash
cd /c/Users/Pichau/PycharmProjects/manim-fisica
D=videos_longos/yt_0006_magnetostatica_biot_savart; R=$D/renders
rm -rf $R/iv; mkdir -p $R/iv; cp -r $R/f1/Tex $R/iv/Tex; rm -f $D/intervalos.jsonl $D/eventos_sync.jsonl $R/intervalos_done.txt
SEG=nenhuma SYNC_LOG=$D/intervalos.jsonl QA_EVENTS=$D/eventos_sync.jsonl uv run python -m manim -r 960,540 --fps 15 --media_dir $R/iv $D/cena.py YT0006BiotSavart > $R/iv/log.txt 2>&1
echo "iv exit $?" > $R/intervalos_done.txt
