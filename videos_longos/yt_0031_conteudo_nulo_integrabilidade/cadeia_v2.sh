#!/bin/bash
# yt_0031 v2: secas → ritmo → render de todos os lotes → montagem → prancha → QA. uso: ./cadeia_v2.sh > renders/v2/qa/cadeia.txt
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8 RODADA=v2
T0=$(date +%s)
rm -f ritmo31.json
printf "%s\n" PB7 PB1 PB6 PB4 PB3 PS PH PB8 PB2 PB5 PB9 PA | xargs -P 4 -I{} ./seco.sh {}
for L in PH PA PB1 PB2 PB3 PB4 PB5 PB6 PB7 PB8 PB9 PS; do grep -q Traceback log_seco_$L.txt && echo "ERRO seco $L"; done
"$PY" ritmo31.py
echo "seco+ritmo $(( $(date +%s)-T0 ))s"
rm -rf threejs/q3d threejs/pedidos3d
./render_todos.sh
"$PY" montar.py && "$PY" comparar.py --tudo && "$PY" qa31v2.py
echo "total $(( $(date +%s)-T0 ))s"
