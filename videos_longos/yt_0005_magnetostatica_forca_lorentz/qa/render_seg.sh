#!/bin/bash
# uso: qa/render_seg.sh SEG FPS NOME   (renderiza só a seção SEG em 960x540 e copia para renders/final6/NOME.mp4)
cd "$(dirname "$0")/../../.."
U=videos_longos/yt_0005_magnetostatica_forca_lorentz
M=$U/renders/final6/media
if [ "$1" = "ALL" ]; then unset SEG; else export SEG=$1; fi
START=$(date +%s)
uv run python -m manim -r 960,540 --fps $2 --media_dir $M -o $3.mp4 $U/cena.py YT0005MagnetostaticaM1 > $U/renders/final6/$3.log 2>&1
cp $M/videos/cena/540p$2/$3.mp4 $U/renders/final6/$3.mp4
echo "$3 pronto em $(( $(date +%s) - START ))s: $(grep -ciE 'error|traceback' $U/renders/final6/$3.log) erros no log" >> $U/renders/final6/render_status.txt
