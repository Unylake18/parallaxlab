#!/bin/bash
# yt_0024 onda 2: lotes em ondas de no máximo 3 (a CPU está dividida com outro job); log em ondas_w2.log
cd "$(dirname "$0")"
onda() { for L in "$@"; do case $L in PB3|PB5) ./render.sh $L > run_$L.txt 2>&1 & ;; *) ./render3d.sh $L > run_$L.txt 2>&1 & ;; esac; done; wait; }
date > ondas_w2.log
onda PB6 PB1 PB4; echo "A $(date)" >> ondas_w2.log
onda PB2 PH PS; echo "B $(date)" >> ondas_w2.log
onda PB3 PB5; echo "C $(date)" >> ondas_w2.log
for L in PH PB1 PB2 PB3 PB4 PB5 PB6 PS; do echo "$L $(grep -a '\[tempo\] total' log_$L.txt) tb=$(grep -ac Traceback log_$L.txt)" >> ondas_w2.log; done
