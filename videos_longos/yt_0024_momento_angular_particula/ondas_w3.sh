#!/bin/bash
cd "$(dirname "$0")"
date > ondas_w3.log
for L in PB6 PB4 PB1; do ./render3d.sh $L > run_$L.txt 2>&1 & done; wait
echo "D $(date)" >> ondas_w3.log
