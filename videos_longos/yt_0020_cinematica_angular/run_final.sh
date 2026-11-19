#!/bin/bash
# yt_0020 render FINAL 1920×1080/30 em ondas de 3 lotes; depois emenda o master visual. Limpa media_F_* e q3d/*_1920x1080 ao fim.
cd "$(dirname "$0")"
rm -f log_final.txt
for W in "PH PT1 PT2" "PT3 PT4 PT5" "PE1 PE2 PE3" "PS"; do
  for L in $W; do ./render_f1080.sh $L > log_Frun_$L.txt 2>&1 & done
  wait
  echo "onda $W concluída $(date +%H:%M:%S)" >> log_final.txt
done
PY=../../.venv/Scripts/python.exe
PYTHONIOENCODING=utf-8 $PY montar_final1080.py v1 > log_final_montar.txt 2>&1
echo FIM >> log_final.txt
