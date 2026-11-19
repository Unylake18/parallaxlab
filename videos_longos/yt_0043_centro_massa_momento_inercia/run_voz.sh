#!/bin/bash
# yt_0043 §5: uma tomada completa (5 blocos). A chave vem do ambiente (nunca de arquivo).
cd /k/PycharmProjects/manim-fisica
export PYTHONIOENCODING=utf-8
U=videos_longos/yt_0043_centro_massa_momento_inercia
.venv/Scripts/python.exe videos/gerar_voz_elevenlabs.py $U/narracao_tags.md $U/audio/narracao_v1.wav --voz qw7jgPZWOKrl10GsjQ82 --secao "## Texto corrido (para gravação)" > $U/log_voz.txt 2>&1
echo FIM >> $U/log_voz.txt
