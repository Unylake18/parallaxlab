#!/bin/bash
cd "$(dirname "$0")"
date > ondas_w4.log
./render.sh PB5 > run_PB5.txt 2>&1 &
./render.sh PB4 > run_PB4.txt 2>&1 &
wait
echo "E $(date)" >> ondas_w4.log
