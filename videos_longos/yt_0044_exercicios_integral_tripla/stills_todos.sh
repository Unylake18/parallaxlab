#!/bin/bash
# yt_0044 final: stills 1080p nativos de todas as marcas dos lotes dados (marca − 0,02 s), em sequência. uso: ./stills_todos.sh LOTE...
cd "$(dirname "$0")"
PY="K:/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
for L in "$@"; do
  for t in $(grep "^\[marca\]" log_$L.txt | awk '{print $3}'); do
    T=$("$PY" -c "print(f'{float(\"$t\") - 0.02:.3f}')")
    ./still.sh "$L" "$T" > /dev/null 2>&1
  done
  echo "[stills] $L ok"
done
echo FIM_STILLS
