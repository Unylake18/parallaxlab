#!/bin/bash
# yt_0020 v7: medição (SYNC=medir) dos lotes de timing alterado e render do preview 540p com fundo de estrelas, em ondas.
# 3D regenerado só onde o tempo ou o desenho 3D mudou (PT4, PT5, PE3); PH e PS reaproveitam os PNGs.
cd "$(dirname "$0")"
rm -f log_v7_ondas.txt
for L in PH PT1 PT4 PT5 PE3; do ./medir.sh $L > /dev/null 2>&1 & done
wait
echo "medição concluída $(date +%H:%M:%S)" >> log_v7_ondas.txt
for W in "PT4 PT5 PE3" "PH PS PE1" "PE2 PT1 PT2" "PT3"; do
  for L in $W; do
    case $L in PH|PS) ./render_v3.sh $L --sem3d > log_v7run_$L.txt 2>&1 & ;; *) ./render_v3.sh $L > log_v7run_$L.txt 2>&1 & ;; esac
  done
  wait
  echo "onda $W concluída $(date +%H:%M:%S)" >> log_v7_ondas.txt
done
echo FIM >> log_v7_ondas.txt
