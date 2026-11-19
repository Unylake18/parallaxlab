#!/bin/bash
# yt_0031 v3: (secas e ritmo já feitos) render de todos os lotes → montagem → prancha → QA → cortes e costuras. uso: ./cadeia_v3.sh > renders/v3/qa/cadeia.txt
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8 RODADA=v3
T0=$(date +%s)
[ $# -eq 0 ] && rm -rf threejs/q3d threejs/pedidos3d   # com lotes nomeados, o cache 3D dos outros lotes fica (QA de alinhamento)
./render_todos.sh ${@}
"$PY" montar.py && "$PY" comparar.py --tudo && "$PY" qa31v3.py && "$PY" qa31v3.py --extra
echo "total $(( $(date +%s)-T0 ))s"
