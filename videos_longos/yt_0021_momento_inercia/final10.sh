cd K:/PycharmProjects/manim-fisica/videos_longos/yt_0021_momento_inercia
PY=../../.venv/Scripts/python.exe; export PYTHONIOENCODING=utf-8
rm -f renders/_final10.flag
# render final 1080p30: 4 lotes de cada vez (os 3D primeiro, que são os mais pesados)
printf '%s\n' PT5 PT4 PT6 PH PE3 PE1 PE2 PT1 PT2 PT3 PA PS | xargs -P 4 -I{} ./render_f1080.sh {} > renders/render_final10.log 2>&1
$PY montar_final21.py > renders/montar_final10.log 2>&1
$PY ../../videos/montar_master.py renders/master_mudo_yt0021_1920x1080.mp4 audio/narracao_v4.wav renders/master_yt0021_1920x1080.mp4 > renders/master10.log 2>&1
$PY gerar_srt21.py > renders/srt10.log 2>&1
echo FIM > renders/_final10.flag
