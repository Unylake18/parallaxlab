#!/bin/bash
cd /c/Users/Pichau/PycharmProjects/manim-fisica
M='C:\Users\Pichau\AppData\Local\Temp\claude\C--Users-Pichau-PycharmProjects-manim-fisica\4009e9b8-d068-4cdb-b5eb-d7a7df007a5e\scratchpad\media24'
MEDIA_DIR="$M" uv run --no-sync python -m manim -ql -r 540,960 --fps 15 videos/vid_0024_carga_helice/cena_final.py CargaHelice024 > videos/vid_0024_carga_helice/render_sync.log 2>&1
echo done >> videos/vid_0024_carga_helice/render_sync.log
