#!/bin/bash
# Preview único do acabamento: espera a fumaça (f1), renderiza por trechos (n1..n8) e junta.
cd /c/Users/Pichau/PycharmProjects/manim-fisica
D=videos_longos/yt_0006_magnetostatica_biot_savart
R=$D/renders
LOG=$R/acabamento.log
until grep -q "f1 exit" /c/Users/Pichau/AppData/Local/Temp/claude/C--Users-Pichau-PycharmProjects-manim-fisica/ee3e99a4-cfb1-4403-bb86-62a7fae14c0b/tasks/bznj7zi9w.output 2>/dev/null; do sleep 10; done
echo "[$(date)] fumaça ok" > $LOG
run() { n=$1; shift; rm -rf $R/$n; mkdir -p $R/$n; cp -r $R/f1/Tex $R/$n/Tex; bash $D/_grupo.sh $n "$1" >> $LOG 2>&1; }
run n1 abertura,regime,geometria,lei
run n2 distribuidas,clinica
run n3 superposicao,metodo
run n4 trecho
run n5 infinito,fios
run n6 espira,algebra_espira
run n7 centro,distante
run n8 sintese,fechamento
V=$R/preview/YT0006BiotSavart_acabamento.mp4
rm -f $V
uv run python $D/juntar.py $V $(for c in n1 n2 n3 n4 n5 n6 n7 n8; do echo $R/$c/videos/cena/540p15/YT0006BiotSavart.mp4; done) >> $LOG 2>&1
echo "[$(date)] CONCLUIDO: $V" >> $LOG
echo CONCLUIDO > $R/acabamento_done.txt
