#!/bin/bash
cd "$(dirname "$0")"
for L in PB3 PB4 PS; do ./render3d.sh $L > fila_b_$L.txt 2>&1; echo "$L feito $(date +%H:%M:%S)" >> fila_b.log; done
