#!/bin/bash
# passagem seca (PEDIDOS3D=1) de vários lotes: pega erros de código e grava os pedidos 3D. uso: ./seco_v3.sh PH P7 ...
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
for C in "$@"; do
  PEDIDOS3D=1 MEDIA_DIR="$PWD/media_ped_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --dry_run cena.py $C > "log_ped_$C.txt" 2>&1
  echo "$C: $(grep -c Traceback log_ped_$C.txt) erros; $(grep '\[tempo\] total\|\[3d\]' log_ped_$C.txt | tr '\n' ' ')"
done
