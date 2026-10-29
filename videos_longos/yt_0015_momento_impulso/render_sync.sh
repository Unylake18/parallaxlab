#!/bin/bash
# sincronia fina: todos os lotes com SYNC=1 (sync/mapa.json + ritmo.json), camadas 3D, composições e montagem com a voz
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
export SYNC=1
lote(){ for c in "$@"; do ( AUDITORIA=1 ANCORAS=1 ./render.sh $c > /dev/null ) & done; wait; }
lote PT1 PD PE PG PT3
lote PA PB PC PF PS
( AUDITORIA=1 ./render.sh PH -t & AUDITORIA=1 ./render.sh PG4 -t & AUDITORIA=1 ./render.sh PF2 -t & wait )
for c in PA PT1 PB PT3 PC PD PE PF PG PS PH PG4 PF2; do echo "== $c: $(grep -c Traceback log_$c.txt) erros; $(grep -h '\[sync\]\|camada\]' log_$c.txt | tr '\n' ' ')"; done
"$PY" compor.py --trecho hook --classe PH | tail -1
"$PY" compor.py --trecho e4 --classe PG4 | tail -1
"$PY" compor.py --trecho cavalo --classe PF2 | tail -1
"$PY" montar_sync.py
