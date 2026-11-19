cd K:/PycharmProjects/manim-fisica/videos_longos/yt_0021_momento_inercia
PY=../../.venv/Scripts/python.exe; export PYTHONIOENCODING=utf-8
rm -f renders/_final9b.flag
$PY parado21.py v9 3 > renders/_parado_run.txt 2>&1; $PY coluna21.py v9 > renders/_coluna_run.txt 2>&1
for C in PH PA PT1 PT2 PT3 PT4 PT5 PT6 PE1 PE2 PE3 PS; do ./auditar.sh $C > /dev/null 2>&1 & done; wait
$PY agrupar_portao.py >/dev/null 2>&1; $PY classifica_portao.py > renders/_cls.txt 2>&1; $PY revisa_portao.py > renders/_rev.txt 2>&1
$PY qa21.py > renders/_qa_run.txt 2>&1; $PY algebra21.py >/dev/null 2>&1; $PY equacao21.py > /dev/null 2>&1
$PY ordem_folhas.py v9 > renders/_ordem.txt 2>&1
echo FIM > renders/_final9b.flag
