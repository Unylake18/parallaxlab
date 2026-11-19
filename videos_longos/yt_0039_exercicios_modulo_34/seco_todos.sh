#!/bin/bash
cd "$(dirname "$0")"
export RODADA=final
for c in PH PA PE1 PE2 PE3 PE4 PE5 PE6 PS; do ./seco.sh $c > "seco_out_$c.txt" 2>&1 & done
wait
echo feito > seco_todos.ok
