#!/bin/bash
# sincronia: só os 10 lotes Manim (camadas 3D inalteradas) → montagem com a voz → medida de parado
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
export SYNC=1
lote(){ for c in "$@"; do ( AUDITORIA=1 ANCORAS=1 ./render.sh $c > /dev/null ) & done; wait; }
lote PT1 PD PE PG PT3
lote PA PB PC PF PS
for c in PA PT1 PB PT3 PC PD PE PF PG PS; do echo "== $c: $(grep -c Traceback log_$c.txt) erros; $(grep -h '\[sync\]' log_$c.txt) $(grep -c '^\[audit\]\|^\[orfao\]' log_$c.txt) sobrep/órfãos"; done
"$PY" montar_sync.py | tail -14
"$PY" medir_parado.py renders/preview_yt0015_sync_960x540.mp4 6 | grep "v6\]"
