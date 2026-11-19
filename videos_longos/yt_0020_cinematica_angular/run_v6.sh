#!/bin/bash
# yt_0020 v6: medição (SYNC=medir) de todos os lotes e depois render com os tempos reais da voz (ancoras.json), em ondas de 3.
cd "$(dirname "$0")"
rm -f log_v6_ondas.txt
for G in "PH PT1 PT2 PT3 PT4" "PT5 PE1 PE2 PE3 PS"; do
  for L in $G; do ./medir.sh $L > /dev/null 2>&1 & done
  wait
done
echo "medição concluída $(date +%H:%M:%S)" >> log_v6_ondas.txt
for W in "PT4 PT5 PE3" "PH PS PE1" "PE2 PT1 PT2" "PT3"; do
  for L in $W; do ./render_v3.sh $L > log_v6run_$L.txt 2>&1 & done
  wait
  echo "onda $W concluída $(date +%H:%M:%S)" >> log_v6_ondas.txt
done
echo FIM >> log_v6_ondas.txt
