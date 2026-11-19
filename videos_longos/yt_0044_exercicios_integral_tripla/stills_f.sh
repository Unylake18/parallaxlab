#!/bin/bash
# yt_0044 final §3: stills 1080p nativos dos quadros afetados pelo F1–F5 (marca − 0,02 s do log do v2) + o quadro 0 do PH. uso: ./stills_f.sh
cd "$(dirname "$0")"
PY="K:/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
mkdir -p renders/final/stills
for par in "PH 01_H1" "PE1 06_E1-4" "PE3 12_E3-1" "PE3 13_E3-2" "PE3 14_E3-3" "PE4 16_E4-1" "PE4 17_E4-2" "PE5 19_E5-1" "PE5 20_E5-2" "PS 26_S2"; do
  set -- $par; L=$1; A=$2
  t=$(grep "^\[marca\] $A " log_$L.txt | awk '{print $3}')
  T=$("$PY" -c "print(f'{float(\"$t\") - 0.02:.3f}')")
   ./still.sh "$L" "$T" > /dev/null 2>&1; cp "renders/still/${L}_$T.png" "renders/final/stills/$A.png"

done

echo FIM_STILLS_F
