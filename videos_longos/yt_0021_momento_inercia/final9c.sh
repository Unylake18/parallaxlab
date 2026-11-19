cd K:/PycharmProjects/manim-fisica/videos_longos/yt_0021_momento_inercia
PY=../../.venv/Scripts/python.exe; export PYTHONIOENCODING=utf-8
rm -f renders/_final9c.flag
while [ ! -f renders/_final9b.flag ]; do sleep 10; done
./medir.sh PT5 > /dev/null 2>&1
./render_todos.sh PT5 > renders/render_v9c.log 2>&1
$PY montar_preview.py v9 > renders/montar_v9.log 2>&1
$PY montar_voz.py v9 > renders/voz_v9.log 2>&1
$PY sync21.py > renders/_sync_run.txt 2>&1
$PY folhas_sync21.py v9 > renders/_folhas_run.txt 2>&1
$PY parado21.py v9 3 > renders/_parado_run.txt 2>&1; $PY coluna21.py v9 > renders/_coluna_run.txt 2>&1
./auditar.sh PT5 > /dev/null 2>&1
$PY agrupar_portao.py >/dev/null 2>&1; $PY classifica_portao.py > renders/_cls.txt 2>&1; $PY revisa_portao.py > renders/_rev.txt 2>&1
$PY qa21.py > renders/_qa_run.txt 2>&1; $PY algebra21.py >/dev/null 2>&1; $PY equacao21.py > /dev/null 2>&1
$PY ordem_folhas.py v9 > renders/_ordem.txt 2>&1
echo FIM > renders/_final9c.flag
