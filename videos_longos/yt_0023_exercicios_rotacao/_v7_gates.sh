#!/bin/bash
cd "$(dirname "$0")"
export PYTHONIOENCODING=utf-8
for L in PH PE1a PE1b PE2 PE3 PE4 PS; do
  uv run --no-sync python flash23.py $L renders/v7/flash_$L.txt > renders/v7/_fl_$L.log 2>&1
  uv run --no-sync python gates_v4.py $L renders/v7/gates_$L.txt > renders/v7/_gt_$L.log 2>&1
done
echo done > renders/v7/_gates_fim.txt
