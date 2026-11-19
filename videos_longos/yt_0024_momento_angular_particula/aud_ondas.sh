#!/bin/bash
cd "$(dirname "$0")"
onda() { for L in "$@"; do ./auditar.sh $L > /dev/null 2>&1 & done; wait; }
onda PB6 PH PB3; onda PB1 PB2 PB5; onda PB4 PS
for L in PH PB1 PB2 PB3 PB4 PB5 PB6 PS; do echo "$L $(grep -a '\[tempo\] total' log_aud_$L.txt) aud=$(grep -ac '\[audit\]' log_aud_$L.txt) tb=$(grep -ac Traceback log_aud_$L.txt)"; done > aud.done
