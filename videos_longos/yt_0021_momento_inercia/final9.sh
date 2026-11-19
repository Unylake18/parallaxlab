cd K:/PycharmProjects/manim-fisica/videos_longos/yt_0021_momento_inercia
PY=../../.venv/Scripts/python.exe; export PYTHONIOENCODING=utf-8
rm -f renders/_final9.flag
for C in PH PA PT1 PT2 PT3 PT4 PT5 PT6 PE1 PE2 PE3 PS; do ./medir.sh $C > /dev/null 2>&1 & done; wait
grep -h "gatilho-sem-frase\|Traceback" log_med_*.txt | sort -u > renders/sem_frase_v9.txt
./render_todos.sh PH PA PT1 PT2 PT3 PT4 PT5 PT6 PE1 PE2 PE3 PS > renders/render_v9.log 2>&1
$PY montar_preview.py v9 > renders/montar_v9.log 2>&1
$PY montar_voz.py v9 > renders/voz_v9.log 2>&1
$PY sync21.py > renders/_sync_run.txt 2>&1
echo FIM > renders/_final9.flag
