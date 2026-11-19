#!/bin/bash
# renderiza todos os lotes em ondas de no máximo 3 (3D com render3d.sh); log em ondas.log
cd "$(dirname "$0")"
onda() { for L in "$@"; do case $L in PH|PE1a|PE1b|PE3) ./render3d.sh $L > run_$L.txt 2>&1 & ;; *) ./render.sh $L > run_$L.txt 2>&1 & ;; esac; done; wait; }
date > ondas.log
onda PH PE1a PE1b; echo "onda 1 $(date)" >> ondas.log
onda PE3 PE1b; echo "onda 2 $(date)" >> ondas.log

for L in PH PE1a PE1b PE2 PE3 PE4 PS; do echo "$L $(grep -a '\[tempo\] total' log_$L.txt) $(grep -ac Traceback log_$L.txt)" >> ondas.log; done
