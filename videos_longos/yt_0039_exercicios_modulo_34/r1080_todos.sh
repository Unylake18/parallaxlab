#!/bin/bash
cd "$(dirname "$0")"
./render1080_fila.sh PE4 PE2 PH PA > r1080_a.txt 2>&1 &
./render1080_fila.sh PE5 PE1 PS > r1080_b.txt 2>&1 &
./render1080_fila.sh PE6 PE3 > r1080_c.txt 2>&1 &
wait
echo feito > r1080.ok
