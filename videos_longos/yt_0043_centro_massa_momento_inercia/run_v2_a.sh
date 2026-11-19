#!/bin/bash
cd "$(dirname "$0")"
for L in PH PB1 PB2; do ./render3d.sh $L > fila_a_$L.txt 2>&1; echo "$L feito $(date +%H:%M:%S)" >> fila_a.log; done
./render.sh PA > fila_a_PA.txt 2>&1; echo "PA feito $(date +%H:%M:%S)" >> fila_a.log
