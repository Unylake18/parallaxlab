#!/bin/bash
# v6.1: todos os lotes (âncoras da narração v5.3) em duas levas de até 6, camadas 3D, composições e montagem
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
./render_lote_v6.sh PT1 PD PE PG PT3 PC
( ./render_lote_v6.sh PA PB PF PS & AUDITORIA=1 ./render.sh PH -t & AUDITORIA=1 ./render.sh PG4 -t & AUDITORIA=1 ./render.sh PF2 -t & wait )
for c in PH PG4 PF2; do echo "== $c $(grep -c Traceback log_$c.txt) erros; $(grep 'camada\]' log_$c.txt)"; done
"$PY" compor.py --trecho hook --classe PH | tail -1
"$PY" compor.py --trecho e4 --classe PG4 | tail -1
"$PY" compor.py --trecho cavalo --classe PF2 | tail -1
"$PY" montar_preview.py | tail -c 400
