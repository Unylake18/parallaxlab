#!/bin/bash
# yt_0024: todos os lotes em ondas de no máximo 3 (3D com render3d.sh); log em ondas.log
cd "$(dirname "$0")"
onda() { for L in "$@"; do case $L in PB3|PB5) ./render.sh $L > run_$L.txt 2>&1 & ;; *) ./render3d.sh $L > run_$L.txt 2>&1 & ;; esac; done; wait; }
date > ondas.log
onda PB6 PH PB3; echo "onda 1 $(date)" >> ondas.log
onda PB1 PB2 PB5; echo "onda 2 $(date)" >> ondas.log
onda PB4 PS; echo "onda 3 $(date)" >> ondas.log
for L in PH PB1 PB2 PB3 PB4 PB5 PB6 PS; do echo "$L $(grep -a '\[tempo\] total' log_$L.txt) tb=$(grep -ac Traceback log_$L.txt) $(tail -n1 log_3d_$L.txt 2>/dev/null)" >> ondas.log; done
