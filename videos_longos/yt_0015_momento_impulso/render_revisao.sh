#!/bin/bash
# revisão GPT (A1–A3, B1–B4): e4 3D (entrada 0,2 s), regrava PT3 PB PE, ritmo, re-render dos lotes afetados, montagem, parado
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
export CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"
"$PY" gerar_timelines.py > /dev/null
( cd threejs && rm -rf frames3d_e4_960x540 && node render3d.js --trecho e4 | tail -1 )
export SYNC=1
for c in PT3 PB PE; do ( SYNC_REC=1 ./render.sh $c --dry_run > /dev/null ) & done; wait
for c in PT3 PB PE; do echo "rec $c: $(grep -c Traceback log_$c.txt) erros"; done
"$PY" ritmo.py | sed -n '/atrasos/,/esperas/p'
lote(){ for c in "$@"; do ( AUDITORIA=1 ANCORAS=1 ./render.sh $c > /dev/null ) & done; wait; }
lote PT3 PE PG PD PT1
lote PB PC PF
AUDITORIA=1 ./render.sh PG4 -t > /dev/null
for c in PT1 PB PT3 PC PD PE PF PG PG4; do echo "== $c: $(grep -c Traceback log_$c.txt) erros; $(grep -h '\[sync\]\|camada\]' log_$c.txt | tr '\n' ' ') $(grep -c '^\[audit\]\|^\[orfao\]' log_$c.txt) sobrep/órfãos"; done
grep -h "^\[audit\]\|^\[orfao\]\|^\[atraso\]" log_P*.txt
"$PY" compor.py --trecho e4 --classe PG4 | tail -1
"$PY" montar_sync.py | tail -14
"$PY" medir_parado.py renders/preview_yt0015_sync_960x540.mp4 6 | grep "v6\]"
