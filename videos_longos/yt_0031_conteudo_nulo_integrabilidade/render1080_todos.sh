#!/bin/bash
# yt_0031 final §8: todos os lotes em 1920×1080 @ 30 fps (CRF 14 pelo template/qualidade.py), P em paralelo, timeout por lote.
# uso: P=4 ./render1080_todos.sh [LOTES...]
cd "$(dirname "$0")"
L=${@:-PB7 PB1 PB6 PB2 PB3 PB4 PS PB5 PH PB8 PB9 PA}
printf "%s\n" $L | xargs -P ${P:-4} -I{} bash -c 'timeout 10800 ./render1080.sh {} > /dev/null 2>&1; echo "[lote1080] {} $?"'
echo "[render1080_todos fim]"
