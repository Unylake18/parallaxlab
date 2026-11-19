cd K:/PycharmProjects/manim-fisica/videos_longos/yt_0021_momento_inercia
rm -f renders/_final9d.flag
bash ./final9.sh
bash ./final9b.sh
PY=../../.venv/Scripts/python.exe; export PYTHONIOENCODING=utf-8
$PY folhas_sync21.py v9 > renders/_folhas_run.txt 2>&1
echo FIM > renders/_final9d.flag
