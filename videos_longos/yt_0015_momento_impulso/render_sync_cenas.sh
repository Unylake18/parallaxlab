#!/bin/bash
# sincronia (cenas novas nas demoras): regrava PT1 PC PD PE, refaz o ritmo, renderiza esses 4, monta e mede o parado
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
export SYNC=1
L="PT1 PC PD PE"
for c in $L; do ( SYNC_REC=1 ./render.sh $c --dry_run > /dev/null ) & done; wait
for c in $L; do echo "rec $c: $(grep -c Traceback log_$c.txt) erros"; done
"$PY" ritmo.py | sed -n '/atrasos/,/esperas/p'
for c in $L; do ( AUDITORIA=1 ANCORAS=1 ./render.sh $c > /dev/null ) & done; wait
for c in $L; do echo "== $c: $(grep -c Traceback log_$c.txt) erros; $(grep -h '\[sync\]' log_$c.txt) $(grep -c '^\[audit\]\|^\[orfao\]' log_$c.txt) sobrep/órfãos"; done
grep -h "^\[audit\]\|^\[orfao\]\|^\[atraso\]" log_PT1.txt log_PC.txt log_PD.txt log_PE.txt
"$PY" montar_sync.py | tail -14
"$PY" medir_parado.py renders/preview_yt0015_sync_960x540.mp4 6 | grep "v6\]"
