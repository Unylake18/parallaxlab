#!/bin/bash
# junta g1..g7 + teste(g8) e a voz → renders/final/master_yt0006.mp4
cd /c/Users/Pichau/PycharmProjects/manim-fisica
D=videos_longos/yt_0006_magnetostatica_biot_savart; F=$D/renders/final
t() { echo $F/$1/videos/cena/1080p30/YT0006BiotSavart.mp4; }
uv run --no-sync python $D/montar_final.py $F/master_yt0006.mp4 $(t g1) $(t g2) $(t g3) $(t g4) $(t g5) $(t g6) $(t g7) $(t teste)
