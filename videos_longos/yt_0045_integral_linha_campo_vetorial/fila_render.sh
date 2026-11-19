#!/bin/bash
cd "$(dirname "$0")"
rm -f fila_render.done
for C in PH PA PB1 PB2 PB4; do ./render.sh $C > /dev/null 2>&1 & done
wait
for C in PB5 PB6 PB7 PS; do ./render.sh $C > /dev/null 2>&1 & done
wait
echo ok > fila_render.done
