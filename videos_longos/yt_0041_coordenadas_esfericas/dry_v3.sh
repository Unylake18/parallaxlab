#!/bin/bash
# passagem seca de todos os lotes (PEDIDOS3D=1): acha erros de código/gatilho antes do render
cd "$(dirname "$0")"
PY="K:/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8 RODADA=v3
for C in PH PA PB1 PB2 PB3 PB4 PB5 PB6 PB7 PS; do
  PEDIDOS3D=1 MEDIA_DIR="$PWD/media_ped_$C" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none --dry_run --disable_caching cena.py $C > "log_ped_$C.txt" 2>&1
  if grep -q "Traceback" "log_ped_$C.txt"; then echo "FALHA $C"; grep -n "Error" "log_ped_$C.txt" | tail -n 3; else echo "ok $C"; fi
done
echo FIM_DRY
