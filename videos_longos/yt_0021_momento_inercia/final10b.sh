cd K:/PycharmProjects/manim-fisica/videos_longos/yt_0021_momento_inercia
PY=../../.venv/Scripts/python.exe; export PYTHONIOENCODING=utf-8
rm -f renders/_final10b.flag
while [ ! -f renders/_final9d.flag ]; do sleep 20; done
./render_f1080.sh PE2 > renders/render_final10b.log 2>&1
$PY montar_final21.py > renders/montar_final10.log 2>&1
$PY ../../videos/montar_master.py renders/master_mudo_yt0021_1920x1080.mp4 audio/narracao_v4.wav renders/master_yt0021_1920x1080.mp4 > renders/master10.log 2>&1
$PY gerar_srt21.py > renders/srt10.log 2>&1
LOGPFX=log_F_ SYNCOUT=sync_final.txt $PY sync21.py > renders/_sync_final_run.txt 2>&1
echo FIM > renders/_final10b.flag
