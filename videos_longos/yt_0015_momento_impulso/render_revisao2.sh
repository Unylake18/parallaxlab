#!/bin/bash
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
export SYNC=1
SYNC_REC=1 ./render.sh PT3 --dry_run > /dev/null; echo "rec PT3: $(grep -c Traceback log_PT3.txt) erros"
"$PY" ritmo.py | sed -n '/atrasos/,/esperas/p'
for c in PT3 PE; do ( AUDITORIA=1 ANCORAS=1 ./render.sh $c > /dev/null ) & done; wait
for c in PT3 PE; do echo "== $c: $(grep -c Traceback log_$c.txt) erros; $(grep -h '\[sync\]' log_$c.txt) $(grep -c '^\[audit\]\|^\[orfao\]' log_$c.txt) sobrep/órfãos"; done
grep -h "^\[audit\]\|^\[orfao\]\|^\[atraso\]" log_PT3.txt log_PE.txt
"$PY" montar_sync.py | tail -3
