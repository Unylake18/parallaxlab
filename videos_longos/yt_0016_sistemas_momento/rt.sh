#!/bin/bash
# teste direto de uma seção: ./rt.sh sec_t7 LoteT7 → media_t_<Lote>/..., log_t_<Lote>.txt
cd "$(dirname "$0")"
PY="C:/Users/Pichau/PycharmProjects/manim-fisica/.venv/Scripts/python.exe"
export PYTHONIOENCODING=utf-8
MEDIA_DIR="$PWD/media_t_$2" "$PY" -m manim -r 960,540 --fps 15 --progress_bar none $1.py $2 > "log_t_$2.txt" 2>&1
echo "$2: $(grep -c Error log_t_$2.txt) erros; $(grep '\[tempo\] total' log_t_$2.txt)"
