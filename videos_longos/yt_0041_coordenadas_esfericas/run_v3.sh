#!/bin/bash
cd "$(dirname "$0")"
export RODADA=v3
./render.sh PA > /dev/null 2>&1; echo "PA $(tail -n 1 log_PA.txt)"
for C in PH PB1 PB2 PB3 PB4 PB5 PB6 PB7 PS; do
  ./render3d.sh $C > /dev/null 2>&1
  if grep -q "Traceback" "log_$C.txt"; then echo "FALHA $C"; else echo "ok $C $(tail -n 1 log_$C.txt)"; fi
done
echo FIM_V3
