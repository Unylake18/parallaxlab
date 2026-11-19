#!/bin/bash
# yt_0020 v8: medição (SYNC=medir) dos lotes de timing alterado e render do preview 540p com o fundo do torque, em ondas.
# 3D regenerado onde o desenho 3D mudou (hélice mais escura: PH, PT4, PS; livros: PT5); PE3 reaproveita os PNGs.
cd "$(dirname "$0")"
rm -f log_v8_ondas.txt
for L in PT2 PT5 PE2; do ./medir.sh $L > /dev/null 2>&1 & done
wait
echo "medição concluída $(date +%H:%M:%S)" >> log_v8_ondas.txt
for W in "PT4 PT5 PH" "PS PE1 PE2" "PT1 PT2 PT3" "PE3"; do
  for L in $W; do
    case $L in PE1|PE2|PT1|PT2|PT3|PE3) ./render_v3.sh $L --sem3d > log_v8run_$L.txt 2>&1 & ;; *) ./render_v3.sh $L > log_v8run_$L.txt 2>&1 & ;; esac
  done
  wait
  echo "onda $W concluída $(date +%H:%M:%S)" >> log_v8_ondas.txt
done
echo FIM >> log_v8_ondas.txt
