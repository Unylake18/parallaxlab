#!/bin/bash
cd "$(dirname "$0")"
onda() { for L in "$@"; do ./render3d.sh $L > run_$L.txt 2>&1 & done; wait; }
date > ondas2.log
onda PB6 PH PB1; echo "onda 1 $(date)" >> ondas2.log
onda PB2 PB4 PS; echo "onda 2 $(date)" >> ondas2.log
aud() { for L in "$@"; do ./auditar.sh $L > /dev/null 2>&1 & done; wait; }
aud PB6 PH PB1; aud PB2 PB4 PS; aud PB5
for L in PH PB1 PB2 PB3 PB4 PB5 PB6 PS; do echo "$L $(grep -a '\[tempo\] total' log_$L.txt) tb=$(grep -ac Traceback log_$L.txt) aud=$(grep -ac '\[audit\]' log_aud_$L.txt) $(tail -n1 log_3d_$L.txt 2>/dev/null)" >> ondas2.log; done
