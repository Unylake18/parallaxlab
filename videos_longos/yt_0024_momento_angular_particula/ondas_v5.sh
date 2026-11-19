#!/bin/bash
# yt_0024 v5: render completo dos lotes pedidos (3D + Manim) até 3 em paralelo; depois auditoria + COR OPERADOR de cada um (também em paralelo).
# uso: ./ondas_v5.sh PH PB1 PB3 ...   → run_<L>_v5.txt por lote e ondas_v5.fim ao terminar
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
rm -f ondas_v5.fim
fase1() { ./render3d.sh "$1" > "run_$1_v5.txt" 2>&1; echo "FIM3D" >> "run_$1_v5.txt"; }
fase2() { ./auditar.sh "$1" >> "run_$1_v5.txt" 2>&1; "$PY" corop24.py "$1" > "log_cop_$1.txt" 2>&1; echo "FIM" >> "run_$1_v5.txt"; }
export -f fase1 fase2
export PY
printf "%s\n" "$@" | xargs -P 3 -I{} bash -c 'fase1 {}'
printf "%s\n" "$@" | xargs -P 4 -I{} bash -c 'fase2 {}'
echo FIM > ondas_v5.fim
