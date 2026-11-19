#!/bin/bash
# yt_0044: stills 1920×1080 nativos no instante de cada self.marca(...) do lote (lido do log_<LOTE>.txt) e comparação com o alvo v1.
# O instante passado ao still.sh é a marca − 0,02 s: o STILL para no 1º play/wait com t ≥ STILL, que é o quadro da marca (60,067 → quadro 901 = 60,0667 s).
# uso: ./stills_lote.sh LOTE
cd "$(dirname "$0")"
PY="K:/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
L=$1
grep "^\[marca\]" "log_$L.txt" | while read -r _ alvo t; do
  T=$("$PY" -c "print(f'{float(\"$t\") - 0.02:.3f}')")
  ( timeout 1200 ./still.sh "$L" "$T" > /dev/null 2>&1; f=$(ls referencia/yt_0044_quadros_alvo_$([ "${RODADA:-v1}" = final ] && echo v2 || echo ${RODADA:-v1})/${alvo}_*.jpg | head -1); "$PY" compara.py "$L" "$T" "$(basename "$f")" ) &
done
wait
echo "[stills] $L ok"
