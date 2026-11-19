#!/bin/bash
# yt_0036: render final (voz) de todos os lotes (960×540/15), 2 em paralelo (memória); o PB4 (3D) vai pelo render3d.sh. Timeout de 2 h por lote (vigia de travas).
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 RODADA=final
um() { if [ "$1" = "PB4" ]; then timeout 7200 ./render3d.sh PB4 > /dev/null 2>&1; else timeout 7200 ./render.sh $1 > /dev/null 2>&1; fi; echo "$1 $(grep -o '\[render\] .*' log_$1.txt | tail -1) $(grep -o 'R5-total.*' log_$1.txt) $(grep -o 'flash-total.*' log_$1.txt) MV=$(grep -c '^\[MV\]' log_$1.txt) MARGEM=$(grep -c '^\[MARGEM\]' log_$1.txt) TB=$(grep -c Traceback log_$1.txt)"; }
export -f um
printf "%s\n" PB4 PB5 PB6 PB3 PB1 PH PB2 PB7 PB8 PS PA | xargs -P 2 -I{} bash -c 'um {}'
