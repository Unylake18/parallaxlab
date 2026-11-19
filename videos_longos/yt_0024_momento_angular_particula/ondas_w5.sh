#!/bin/bash
cd "$(dirname "$0")"
date > ondas_w5.log
./render.sh PB2 > run_PB2.txt 2>&1 &
./render.sh PB3 > run_PB3.txt 2>&1 &
wait
echo "F $(date)" >> ondas_w5.log
