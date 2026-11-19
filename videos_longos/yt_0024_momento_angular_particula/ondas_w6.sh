#!/bin/bash
cd "$(dirname "$0")"
date > ondas_w6.log
./render.sh PB3 > run_PB3.txt 2>&1 &
./render.sh PB5 > run_PB5.txt 2>&1 &
./render3d.sh PS > run_PS.txt 2>&1 &
wait
echo "G $(date)" >> ondas_w6.log
