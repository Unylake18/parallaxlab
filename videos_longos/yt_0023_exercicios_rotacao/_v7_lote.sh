#!/bin/bash
cd "$(dirname "$0")"
export PYTHONIOENCODING=utf-8
L=$1; a=$(date +%s)
if [ "$L" = "PS" ]; then ./render.sh PS > run_PS.txt 2>&1; else ./render3d.sh $L > run_$L.txt 2>&1; fi
b=$(date +%s)
./auditar.sh $L > aud_run7_$L.txt 2>&1
c=$(date +%s)
echo "$L render_s=$((b-a)) auditoria_s=$((c-b)) tb=$(grep -ac Traceback log_$L.txt)" > renders/v7/_t_$L.txt
uv run --no-sync python flash23.py $L renders/v7/flash_$L.txt > renders/v7/_fl_$L.log 2>&1
uv run --no-sync python gates_v4.py $L renders/v7/gates_$L.txt > renders/v7/_gt_$L.log 2>&1
