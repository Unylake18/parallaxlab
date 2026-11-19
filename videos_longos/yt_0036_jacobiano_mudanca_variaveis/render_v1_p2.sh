#!/bin/bash
# yt_0036: render v1 de todos os lotes (960×540/15), 3 em paralelo; o PB4 (3D) vai pelo render3d.sh. Timeout de 2 h por lote (vigia de travas).
cd "$(dirname "$0")"
um() { if [ "$1" = "PB4" ]; then timeout 7200 ./render3d.sh PB4 > /dev/null 2>&1; else timeout 7200 ./render.sh $1 > /dev/null 2>&1; fi; echo "$1 $(grep -o '\[render\] .*' log_$1.txt | tail -1) R5=$(grep -c '^\[R5' log_$1.txt) $(grep -o 'flash-total.*' log_$1.txt) $(grep -o 'deriva.*' log_$1.txt | head -1)"; }
export -f um
printf "%s\n" PB4 PB5 PB6 PB3 PB1 PH PB2 PB7 PB8 PS PA | xargs -P 2 -I{} bash -c 'um {}'
