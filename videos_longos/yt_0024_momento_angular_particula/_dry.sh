#!/bin/bash
# passada a seco (só para achar exceções e gerar os pedidos 3D): ./_dry.sh PH PB1 ...
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
for C in "$@"; do
  ( PEDIDOS3D=1 MEDIA_DIR="$PWD/media_ped_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --dry_run cena.py $C > "log_ped_$C.txt" 2>&1; echo "dry $C: $(grep -c Traceback log_ped_$C.txt) tracebacks" >> dry_v5.txt ) &
done
wait
