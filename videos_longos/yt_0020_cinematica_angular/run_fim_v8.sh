#!/bin/bash
cd "$(dirname "$0")"
PY=../../.venv/Scripts/python.exe
export PYTHONIOENCODING=utf-8 CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"
rm -f log_fim7.txt
$PY montar_preview.py v8 > log_mp7.txt 2>&1
$PY mux_voz.py renders/preview_yt0020_v8_960x540.mp4 renders/preview_yt0020_v8_960x540_voz.mp4 > log_mux7.txt 2>&1
$PY sync20.py > log_sync7.txt 2>&1
$PY corop.py PT4 > log_cop_PT4.txt 2>&1
$PY fundo_medida.py renders/preview_yt0020_v8_960x540.mp4 3.0 > log_fundo.txt 2>&1 &
$PY flash20.py renders/preview_yt0020_v8_960x540.mp4 > log_flash.txt 2>&1 &
$PY prancha_humana.py v8 > log_ph7.txt 2>&1
$PY conferencia20.py v8 > log_conf_v8.txt 2>&1
$PY qa20.py v8 > log_qa7.txt 2>&1
wait
echo FIM > log_fim7.txt
