#!/bin/bash
cd "$(dirname "$0")"
rm -f log_final2.txt
./render_f1080.sh PT5 > log_Frun_PT5.txt 2>&1
echo "PT5 concluído $(date +%H:%M:%S)" >> log_final2.txt
PYTHONIOENCODING=utf-8 ../../.venv/Scripts/python.exe montar_final1080.py v1 > log_final_montar.txt 2>&1
PYTHONIOENCODING=utf-8 ../../.venv/Scripts/python.exe ../../videos/montar_master.py renders/master_visual_yt0020_v1_1920x1080.mp4 audio/narracao_v6.wav renders/master_yt0020_1920x1080.mp4 > log_final_master.txt 2>&1
echo FIM >> log_final2.txt
