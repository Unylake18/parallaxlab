#!/bin/bash
cd "$(dirname "$0")"
onda() { for L in "$@"; do case $L in PB3|PB5) ./render.sh $L > run_$L.txt 2>&1 & ;; *) ./render3d.sh $L > run_$L.txt 2>&1 & ;; esac; done; wait; }
aud() { for L in "$@"; do ./auditar.sh $L > /dev/null 2>&1 & done; wait; }
date > ondas3.log
onda PB6 PH PB1; onda PB2 PB4 PS; onda PB5
aud PB6 PH PB1; aud PB2 PB4 PS; aud PB5
for L in PH PB1 PB2 PB3 PB4 PB5 PB6 PS; do echo "$L $(grep -a '\[tempo\] total' log_$L.txt) tb=$(grep -ac Traceback log_$L.txt) aud=$(grep -ac '\[audit\]' log_aud_$L.txt)" >> ondas3.log; done
date >> ondas3.log
