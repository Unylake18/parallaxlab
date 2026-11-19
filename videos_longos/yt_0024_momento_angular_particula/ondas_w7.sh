#!/bin/bash
cd "$(dirname "$0")"
PY="$(cd ../.. && pwd)/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
./render3d.sh PS > run_PS.txt 2>&1 &
for L in PH PB1 PB2 PB3 PB4 PB5 PB6; do
  (./auditar.sh $L > /dev/null 2>&1; "$PY" corop24.py $L > log_cop_$L.txt 2>&1) &
done
wait
(./auditar.sh PS > /dev/null 2>&1; "$PY" corop24.py PS > log_cop_PS.txt 2>&1)
echo FIM > ondas_w7.fim
